#!/usr/bin/env python3
"""Offline integration tests; every destination and modified bundle is temporary.

Run from any directory:
    python3 -m unittest discover -s /path/to/codex-skills/tests -v

These tests install real snapshot files, but never execute a skill or install
anything into the user's real HOME, CODEX_HOME, or agent configuration.
"""

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((REPO / "manifest.json").read_text(encoding="utf-8"))
SKILLS = MANIFEST["skills"]
EXTERNAL_SKILLS = MANIFEST.get("external_skills", [])
DEFAULTS = [skill for skill in SKILLS if skill["kind"] == "local" and skill["enabled"]]
UPSTREAM = next(skill for skill in DEFAULTS if skill["recovery"]["command"])
LOCAL_ONLY = next(skill for skill in DEFAULTS if skill["recovery"]["kind"] == "local-only")
SECOND = next(skill for skill in DEFAULTS if skill["id"] != UPSTREAM["id"])
EXTERNAL = {
    "id": "external-test-plugin",
    "name": "Test plugin",
    "kind": "plugin",
    "summary_zh": "仅提供测试安装入口",
    "plugin_id": "test@catalog",
    "recovery": {
        "command": "codex plugin add test@catalog",
        "source_url": "https://example.test/official-installation",
        "note": "Install through Codex; no plugin files are included.",
    },
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprints(root):
    """Include metadata so an allegedly skipped install cannot rewrite files."""
    return {
        path.relative_to(root).as_posix(): (
            digest(path), stat.S_IMODE(path.stat().st_mode),
            path.stat().st_ino, path.stat().st_mtime_ns,
        )
        for path in root.rglob("*") if path.is_file()
    }


class InstallerIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-skills-tests-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "isolated home"
        self.home.mkdir()
        self.cwd = self.root / "unrelated working directory"
        self.cwd.mkdir()
        self.destination = self.root / "installed skills"
        self.env = os.environ.copy()
        self.env["HOME"] = str(self.home)
        self.env["CODEX_HOME"] = str(self.home / ".codex")
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"

    def run_installer(self, *args, bundle=REPO, destination=True, env=None):
        command = ["bash", str(bundle / "install.sh")]
        if destination:
            command.extend(["--dest", str(self.destination)])
        command.extend(str(arg) for arg in args)
        result = subprocess.run(
            command, cwd=str(self.cwd), env=env or self.env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, timeout=120, check=False,
        )
        return result

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout)

    def assert_payload(self, destination, skill):
        target = destination / skill["install_name"]
        self.assertTrue(target.is_dir(), str(target))
        actual = {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()}
        self.assertEqual(actual, set(skill["files"]), skill["id"])
        for name, metadata in skill["files"].items():
            path = target / name
            self.assertFalse(path.is_symlink(), str(path))
            self.assertEqual(digest(path), metadata["sha256"], str(path))
            expected_mode = 0o755 if metadata["executable"] else 0o644
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), expected_mode, str(path))

    def small_bundle(self, skills=None, name="bundle with spaces"):
        """Copy actual payloads into a mutable temporary bundle."""
        selected = skills if skills is not None else [UPSTREAM, SECOND]
        bundle = self.root / name
        bundle.mkdir()
        (bundle / "scripts").mkdir()
        shutil.copy2(REPO / "install.sh", bundle / "install.sh")
        shutil.copy2(REPO / "scripts/install.py", bundle / "scripts/install.py")
        manifest = copy.deepcopy(MANIFEST)
        manifest["skills"] = copy.deepcopy(selected)
        for skill in selected:
            shutil.copytree(REPO / skill["path"], bundle / skill["path"])
        self.write_manifest(bundle, manifest)
        return bundle, manifest

    def write_manifest(self, bundle, manifest):
        (bundle / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def conflict(self, skill=UPSTREAM):
        target = self.destination / skill["install_name"]
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("previous private local version\n", encoding="utf-8")
        (target / "keep.txt").write_text("do not lose\n", encoding="utf-8")
        return target

    def import_installer(self, bundle):
        spec = importlib.util.spec_from_file_location("isolated_skill_installer", bundle / "scripts/install.py")
        module = importlib.util.module_from_spec(spec)
        with mock.patch.object(sys, "dont_write_bytecode", True):
            spec.loader.exec_module(module)
        return module

    def assert_recovery(self, output, skill):
        self.assertIn("[FAIL] {}:".format(skill["id"]), output)
        self.assertIn("Local retry:", output)
        self.assertIn("--skill " + skill["id"], output)
        if skill["recovery"]["command"]:
            self.assertIn(skill["recovery"]["command"], output)
            self.assertIn("[not executed]", output)
        else:
            self.assertIn("No verified official installation command", output)

    def test_default_installs_every_enabled_local_skill_with_exact_bytes_and_modes(self):
        result = self.run_installer()
        self.assert_success(result)
        self.assertEqual({p.name for p in self.destination.iterdir()}, {s["install_name"] for s in DEFAULTS})
        for skill in DEFAULTS:
            with self.subTest(skill=skill["id"]):
                self.assert_payload(self.destination, skill)
        self.assertIn("{} installed, 0 identical/skipped, 0 planned, 0 failed".format(len(DEFAULTS)), result.stdout)

    def test_repeat_default_install_preserves_bytes_permissions_inodes_and_timestamps(self):
        self.assert_success(self.run_installer())
        before = fingerprints(self.destination)
        result = self.run_installer()
        self.assert_success(result)
        self.assertEqual(fingerprints(self.destination), before)
        self.assertIn("0 installed, {} identical/skipped".format(len(DEFAULTS)), result.stdout)

    def test_bundle_and_destination_with_spaces_work_from_unrelated_cwd(self):
        bundle, _ = self.small_bundle([UPSTREAM])
        result = self.run_installer(bundle=bundle)
        self.assert_success(result)
        self.assert_payload(self.destination, UPSTREAM)

    def test_conflict_preserves_existing_files_and_continues_to_later_skill(self):
        target = self.conflict()
        before = fingerprints(target)
        result = self.run_installer("--skill", UPSTREAM["id"], "--skill", SECOND["id"])
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assert_recovery(result.stdout, UPSTREAM)
        self.assertEqual(fingerprints(target), before)
        self.assert_payload(self.destination, SECOND)
        self.assertIn("1 installed, 0 identical/skipped, 0 planned, 1 failed", result.stdout)

    def test_force_backs_up_conflict_before_installing_exact_payload(self):
        target = self.conflict()
        before = fingerprints(target)
        result = self.run_installer("--skill", UPSTREAM["id"], "--force")
        self.assert_success(result)
        self.assert_payload(self.destination, UPSTREAM)
        backups = list((self.destination.parent / ".codex-skills-backups").iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual(fingerprints(backups[0]), before)
        self.assertIn(str(backups[0]), result.stdout)

    def test_force_rolls_back_when_publishing_staged_directory_fails(self):
        bundle, _ = self.small_bundle([UPSTREAM])
        module = self.import_installer(bundle)
        target = self.conflict()
        before = fingerprints(target)
        real_rename = os.rename

        def fail_publish(source, destination):
            if Path(source).name.startswith(".codex-skills-stage-"):
                raise OSError("simulated publish failure")
            return real_rename(source, destination)

        with mock.patch.object(module.os, "rename", side_effect=fail_publish):
            with self.assertRaisesRegex(module.InstallError, "previous version restored"):
                module.install_one(UPSTREAM, self.destination, force=True)
        self.assertEqual(fingerprints(target), before)
        self.assertFalse(list(self.destination.glob(".codex-skills-stage-*")))
        self.assertFalse(list((self.destination.parent / ".codex-skills-backups").iterdir()))

    def test_force_rolls_back_when_post_publish_validation_fails(self):
        bundle, _ = self.small_bundle([UPSTREAM])
        module = self.import_installer(bundle)
        target = self.conflict()
        before = fingerprints(target)
        real_validate = module.validate_tree

        def fail_after_publish(root, expected):
            if root == target and (root / "SKILL.md").read_bytes() == (bundle / UPSTREAM["path"] / "SKILL.md").read_bytes():
                raise module.InstallError("simulated post-publish verification failure")
            return real_validate(root, expected)

        with mock.patch.object(module, "validate_tree", side_effect=fail_after_publish):
            with self.assertRaisesRegex(module.InstallError, "previous version restored"):
                module.install_one(UPSTREAM, self.destination, force=True)
        self.assertEqual(fingerprints(target), before)
        self.assertFalse(list(self.destination.glob(".codex-skills-stage-*")))

    def test_corrupt_payload_names_failed_skill_prints_upstream_command_and_continues(self):
        bundle, _ = self.small_bundle()
        (bundle / UPSTREAM["path"] / "SKILL.md").write_text("corrupt snapshot", encoding="utf-8")
        result = self.run_installer(bundle=bundle)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assert_recovery(result.stdout, UPSTREAM)
        self.assertIn("SHA-256 mismatch", result.stdout)
        self.assertFalse((self.destination / UPSTREAM["install_name"]).exists())
        self.assert_payload(self.destination, SECOND)

    def test_missing_payload_names_failed_skill_prints_upstream_command_and_continues(self):
        bundle, _ = self.small_bundle()
        shutil.rmtree(bundle / UPSTREAM["path"])
        result = self.run_installer(bundle=bundle)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assert_recovery(result.stdout, UPSTREAM)
        self.assertFalse((self.destination / UPSTREAM["install_name"]).exists())
        self.assert_payload(self.destination, SECOND)

    def test_missing_single_file_fails_only_that_skill(self):
        bundle, _ = self.small_bundle()
        (bundle / UPSTREAM["path"] / "SKILL.md").unlink()
        result = self.run_installer(bundle=bundle)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("missing files: SKILL.md", result.stdout)
        self.assert_recovery(result.stdout, UPSTREAM)
        self.assert_payload(self.destination, SECOND)

    def test_local_only_failure_does_not_invent_an_official_command(self):
        bundle, _ = self.small_bundle([LOCAL_ONLY])
        (bundle / LOCAL_ONLY["path"] / "SKILL.md").unlink()
        result = self.run_installer(bundle=bundle)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assert_recovery(result.stdout, LOCAL_ONLY)
        self.assertNotIn("npx skills add", result.stdout)
        self.assertNotIn("codex plugin add", result.stdout)

    def test_local_retry_command_is_shell_quoted_and_actually_installs_one_skill(self):
        bundle, _ = self.small_bundle([LOCAL_ONLY])
        result = self.run_installer("--recovery", LOCAL_ONLY["id"], bundle=bundle)
        self.assert_success(result)
        self.assertFalse(self.destination.exists())
        retry_line = next(line for line in result.stdout.splitlines() if "Local retry:" in line)
        command = shlex.split(retry_line.split("Local retry:", 1)[1].strip())
        retry = subprocess.run(command, cwd=str(self.cwd), env=self.env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, timeout=120, check=False)
        self.assert_success(retry)
        self.assert_payload(self.destination, LOCAL_ONLY)

    def test_all_installs_every_bundled_payload_and_explains_external_entries(self):
        result = self.run_installer("--all")
        self.assert_success(result)
        self.assertEqual({p.name for p in self.destination.iterdir()}, {s["install_name"] for s in SKILLS})
        for skill in SKILLS:
            with self.subTest(skill=skill["id"]):
                self.assert_payload(self.destination, skill)
        if any(skill["kind"] in ("system", "plugin") for skill in SKILLS):
            self.assertIn("does not install plugin tools, MCP servers, credentials, or bundled runtimes", result.stdout)
        if EXTERNAL_SKILLS:
            self.assertIn("{} external skill(s) have no bundled payload".format(len(EXTERNAL_SKILLS)), result.stdout)
        self.assertNotIn("[EXTERNAL]", result.stdout)
        self.assertIn("{} installed, 0 identical/skipped, 0 planned, 0 failed".format(len(SKILLS)), result.stdout)

    def test_codex_home_selects_default_destination(self):
        custom_home = self.root / "custom Codex home"
        env = dict(self.env, CODEX_HOME=str(custom_home))
        result = self.run_installer("--skill", UPSTREAM["id"], destination=False, env=env)
        self.assert_success(result)
        self.assert_payload(custom_home / "skills", UPSTREAM)
        self.assertFalse(self.destination.exists())
        self.assertFalse((self.home / ".codex").exists())

    def test_unset_codex_home_uses_isolated_home(self):
        env = self.env.copy()
        env.pop("CODEX_HOME", None)
        result = self.run_installer("--skill", UPSTREAM["id"], destination=False, env=env)
        self.assert_success(result)
        self.assert_payload(self.home / ".codex/skills", UPSTREAM)

    def test_destination_symlink_is_rejected_without_writing_through(self):
        external = self.root / "untouched destination"
        external.mkdir()
        (external / "sentinel").write_text("keep", encoding="utf-8")
        self.destination.symlink_to(external, target_is_directory=True)
        before = fingerprints(external)
        result = self.run_installer("--skill", UPSTREAM["id"], "--force")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("Destination directory is a symlink", result.stdout)
        self.assertEqual(fingerprints(external), before)
        self.assertTrue(self.destination.is_symlink())

    def test_individual_skill_symlink_is_not_followed_and_force_backs_up_link(self):
        external = self.root / "untouched skill"
        external.mkdir()
        (external / "SKILL.md").write_text("external", encoding="utf-8")
        self.destination.mkdir()
        target = self.destination / UPSTREAM["install_name"]
        target.symlink_to(external, target_is_directory=True)
        before = fingerprints(external)
        failed = self.run_installer("--skill", UPSTREAM["id"])
        self.assertEqual(failed.returncode, 1, failed.stdout)
        self.assertEqual(fingerprints(external), before)
        self.assertTrue(target.is_symlink())
        result = self.run_installer("--skill", UPSTREAM["id"], "--force")
        self.assert_success(result)
        self.assertEqual(fingerprints(external), before)
        self.assert_payload(self.destination, UPSTREAM)
        backups = list((self.destination.parent / ".codex-skills-backups").iterdir())
        self.assertEqual(len(backups), 1)
        self.assertTrue(backups[0].is_symlink())
        self.assertEqual(backups[0].resolve(), external)

    def test_source_symlink_is_rejected_before_any_installation(self):
        bundle, _ = self.small_bundle()
        source = bundle / UPSTREAM["path"] / "SKILL.md"
        source.unlink()
        external = self.root / "external source.txt"
        external.write_text("external source", encoding="utf-8")
        source.symlink_to(external)
        result = self.run_installer(bundle=bundle)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("forbidden symlink", result.stdout)
        self.assertFalse(self.destination.exists())

    def test_manifest_path_escape_is_rejected_before_any_installation(self):
        for field, value in [("path", "../escape"), ("install_name", "../escape"),
                             ("path", "/absolute/escape"), ("id", "../escape")]:
            with self.subTest(field=field, value=value):
                bundle, manifest = self.small_bundle([UPSTREAM], name="escape-" + str(len(list(self.root.iterdir()))))
                manifest["skills"][0][field] = value
                self.write_manifest(bundle, manifest)
                result = self.run_installer(bundle=bundle)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("Unsafe", result.stdout)
                self.assertFalse(self.destination.exists())
                self.assertFalse((self.root / "escape").exists())

    def test_manifest_file_escape_is_rejected_before_any_installation(self):
        bundle, manifest = self.small_bundle([UPSTREAM])
        manifest["skills"][0]["files"]["../outside.txt"] = copy.deepcopy(UPSTREAM["files"]["SKILL.md"])
        self.write_manifest(bundle, manifest)
        result = self.run_installer(bundle=bundle)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("Unsafe file path", result.stdout)
        self.assertFalse(self.destination.exists())
        self.assertFalse((self.root / "outside.txt").exists())

    def test_bundle_overlap_is_rejected_for_same_child_parent_and_normalized_path(self):
        bundle, _ = self.small_bundle([UPSTREAM])
        before = fingerprints(bundle)
        for destination in [bundle, bundle / "new skills", bundle.parent,
                            bundle / "never-created" / ".." / "new skills"]:
            with self.subTest(destination=str(destination)):
                self.destination = destination
                result = self.run_installer(bundle=bundle)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("must not overlap", result.stdout)
                self.assertEqual(fingerprints(bundle), before)
                self.assertFalse((bundle / "never-created").exists())

    def test_dry_run_and_inventory_do_not_create_destination(self):
        result = self.run_installer("--dry-run")
        self.assert_success(result)
        self.assertIn("{} planned, 0 failed".format(len(DEFAULTS)), result.stdout)
        self.assertFalse(self.destination.exists())
        inventory = self.run_installer("--list")
        self.assert_success(inventory)
        self.assertIn("{} skill(s)".format(len(SKILLS) + len(EXTERNAL_SKILLS)), inventory.stdout)
        self.assertFalse(self.destination.exists())

    def external_bundle(self, selected=None):
        bundle, manifest = self.small_bundle([UPSTREAM] if selected is None else selected)
        manifest["external_skills"] = [copy.deepcopy(EXTERNAL)]
        self.write_manifest(bundle, manifest)
        return bundle, manifest

    def assert_external_instructions(self, result, skill=EXTERNAL):
        self.assertIn(skill["recovery"]["source_url"], result.stdout)
        self.assertIn(skill["recovery"]["note"], result.stdout)
        if skill["recovery"]["command"]:
            self.assertIn(skill["recovery"]["command"], result.stdout)
            self.assertIn("[not executed]", result.stdout)
        self.assertNotIn("Local retry:", result.stdout)

    def test_external_inventory_and_recovery_show_official_entry_without_writes(self):
        bundle, _ = self.external_bundle()
        before = fingerprints(bundle)
        listed = self.run_installer("--list", bundle=bundle)
        self.assert_success(listed)
        self.assertIn("2 skill(s): 1 bundled, 1 external", listed.stdout)
        self.assertIn("{}\tplugin\texternal\tmanual via Codex".format(EXTERNAL["id"]), listed.stdout)
        recovery = self.run_installer("--recovery", EXTERNAL["id"], bundle=bundle)
        self.assert_success(recovery)
        self.assert_external_instructions(recovery)
        self.assertEqual(fingerprints(bundle), before)
        self.assertFalse(self.destination.exists())
        self.assertEqual(list(self.home.iterdir()), [])

    def test_external_selection_does_not_install_or_execute_the_displayed_command(self):
        bundle, manifest = self.external_bundle()
        marker = self.root / "command must not execute"
        command = [sys.executable, "-c", "from pathlib import Path; Path({!r}).touch()".format(str(marker))]
        external = manifest["external_skills"][0]
        external["recovery"]["command"] = " ".join(shlex.quote(part) for part in command)
        self.write_manifest(bundle, manifest)
        before = fingerprints(bundle)
        result = self.run_installer("--skill", external["id"], "--force", bundle=bundle)
        self.assert_success(result)
        self.assert_external_instructions(result, external)
        self.assertIn("[EXTERNAL] " + external["id"], result.stdout)
        self.assertIn("0 installed, 0 identical/skipped, 0 planned, 0 failed, 1 external instructions shown (not installed)", result.stdout)
        self.assertEqual(fingerprints(bundle), before)
        self.assertFalse(marker.exists())
        self.assertFalse(self.destination.exists())
        self.assertFalse((self.destination.parent / ".codex-skills-backups").exists())

    def test_mixed_selection_installs_payload_and_counts_external_instructions_separately(self):
        bundle, _ = self.external_bundle()
        result = self.run_installer("--skill", EXTERNAL["id"], "--skill", UPSTREAM["id"], "--skill", EXTERNAL["id"], bundle=bundle)
        self.assert_success(result)
        self.assert_external_instructions(result)
        self.assert_payload(self.destination, UPSTREAM)
        self.assertEqual({p.name for p in self.destination.iterdir()}, {UPSTREAM["install_name"]})
        self.assertIn("1 installed, 0 identical/skipped, 0 planned, 0 failed, 1 external instructions shown (not installed)", result.stdout)

    def test_default_and_all_skip_external_entries_without_payload_access(self):
        bundle, _ = self.external_bundle()
        default = self.run_installer(bundle=bundle)
        self.assert_success(default)
        self.assert_payload(self.destination, UPSTREAM)
        self.assertNotIn("[EXTERNAL]", default.stdout)
        before = fingerprints(self.destination)
        all_result = self.run_installer("--all", bundle=bundle)
        self.assert_success(all_result)
        self.assertIn("1 external skill(s) have no bundled payload", all_result.stdout)
        self.assertIn("0 installed, 1 identical/skipped, 0 planned, 0 failed, 0 external instructions shown", all_result.stdout)
        self.assertNotIn(EXTERNAL["recovery"]["command"], all_result.stdout)
        self.assertNotIn("[EXTERNAL]", all_result.stdout)
        self.assertEqual(fingerprints(self.destination), before)

    def test_external_only_bundle_all_is_informational_and_does_not_create_destination(self):
        bundle, _ = self.external_bundle([])
        result = self.run_installer("--all", bundle=bundle)
        self.assert_success(result)
        self.assertIn("1 external skill(s) have no bundled payload", result.stdout)
        self.assertIn("0 installed", result.stdout)
        self.assertFalse(self.destination.exists())

    def test_external_without_command_prints_verified_source_without_local_retry(self):
        bundle, manifest = self.external_bundle()
        external = manifest["external_skills"][0]
        external["kind"] = "system"
        external.pop("plugin_id")
        external["recovery"]["command"] = None
        self.write_manifest(bundle, manifest)
        result = self.run_installer("--recovery", external["id"], bundle=bundle)
        self.assert_success(result)
        self.assert_external_instructions(result, external)
        self.assertIn("No verified official installation command", result.stdout)
        self.assertFalse(self.destination.exists())

    def test_legacy_manifest_without_external_skills_remains_installable(self):
        bundle, manifest = self.small_bundle([UPSTREAM])
        manifest.pop("external_skills", None)
        self.write_manifest(bundle, manifest)
        result = self.run_installer(bundle=bundle)
        self.assert_success(result)
        self.assert_payload(self.destination, UPSTREAM)

    def test_unknown_id_in_mixed_external_selection_fails_before_any_write(self):
        bundle, _ = self.external_bundle()
        result = self.run_installer("--skill", EXTERNAL["id"], "--skill", UPSTREAM["id"], "--skill", "does-not-exist", bundle=bundle)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("Unknown skill ID", result.stdout)
        self.assertNotIn("[EXTERNAL]", result.stdout)
        self.assertFalse(self.destination.exists())
        unknown_recovery = self.run_installer("--recovery", "does-not-exist", bundle=bundle)
        self.assertEqual(unknown_recovery.returncode, 2, unknown_recovery.stdout)
        self.assertIn("Unknown skill ID", unknown_recovery.stdout)

    def test_external_duplicate_ids_are_rejected_before_writes(self):
        bundle, manifest = self.external_bundle()
        for collision in ("bundled", "external"):
            with self.subTest(collision=collision):
                changed = copy.deepcopy(manifest)
                if collision == "bundled":
                    changed["external_skills"][0]["id"] = UPSTREAM["id"]
                else:
                    changed["external_skills"].append(copy.deepcopy(EXTERNAL))
                self.write_manifest(bundle, changed)
                result = self.run_installer(bundle=bundle)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("Duplicate skill id:", result.stdout)
                self.assertFalse(self.destination.exists())

    def test_external_invalid_metadata_and_terminal_controls_are_rejected_before_writes(self):
        bundle, manifest = self.external_bundle()
        mutations = [
            ("container", None), ("entry", "invalid"), ("name", 4),
            ("summary_zh", None), ("kind", "local"), ("plugin_id", 7),
            ("path", "must-not-have-payload"), ("recovery", []),
            ("recovery.command", []), ("recovery.source_url", None),
            ("recovery.note", None), ("recovery.command", "command\nsecond command"),
            ("recovery.source_url", "https://example.test/\x1b[2J"),
            ("recovery.note", "invisible\u202ehidden"),
        ]
        for field, value in mutations:
            with self.subTest(field=field, value=repr(value)):
                changed = copy.deepcopy(manifest)
                if field == "container":
                    changed["external_skills"] = value
                elif field == "entry":
                    changed["external_skills"] = [value]
                elif field.startswith("recovery."):
                    changed["external_skills"][0]["recovery"][field.split(".")[1]] = value
                else:
                    changed["external_skills"][0][field] = value
                self.write_manifest(bundle, changed)
                before = fingerprints(bundle)
                result = self.run_installer("--list", bundle=bundle)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertEqual(fingerprints(bundle), before)
                self.assertFalse(self.destination.exists())
                self.assertNotIn("\x1b", result.stdout)

    def test_external_guidance_continues_after_payload_failure(self):
        bundle, _ = self.external_bundle()
        self.conflict()
        before = fingerprints(self.destination)
        result = self.run_installer("--skill", UPSTREAM["id"], "--skill", EXTERNAL["id"], bundle=bundle)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assert_recovery(result.stdout, UPSTREAM)
        self.assertIn("[EXTERNAL] " + EXTERNAL["id"], result.stdout)
        self.assertIn("0 installed, 0 identical/skipped, 0 planned, 1 failed, 1 external instructions shown (not installed)", result.stdout)
        self.assertEqual(fingerprints(self.destination), before)

    def test_unknown_skill_fails_before_any_write(self):
        result = self.run_installer("--skill", "does-not-exist")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("Unknown skill ID", result.stdout)
        self.assertFalse(self.destination.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
