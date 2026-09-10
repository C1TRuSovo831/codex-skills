#!/usr/bin/env python3
"""Validate and install bundled skill files without running them or using a network."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import stat
import sys
import tempfile
from datetime import datetime, timezone
import uuid


BUNDLE = Path(__file__).resolve().parent.parent
SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class InstallError(Exception):
    pass


def safe_name(value, label):
    if not isinstance(value, str) or not SAFE_NAME.fullmatch(value):
        raise InstallError("Unsafe {}: {!r}".format(label, value))
    return value


def relative_path(value, label):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise InstallError("Unsafe {}: {!r}".format(label, value))
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        raise InstallError("Unsafe {}: {!r}".format(label, value))
    return path


def display_text(value, label, allow_empty=False):
    # Metadata is displayed verbatim but never executed. Reject terminal escape,
    # line-breaking, and invisible formatting controls before printing it.
    if not isinstance(value, str) or (not value and not allow_empty) or (value and not value.isprintable()):
        raise InstallError("Invalid display text for {}".format(label))
    return value


def validate_recovery(recovery, identifier, external=False):
    if not isinstance(recovery, dict):
        raise InstallError("Missing recovery metadata: {}".format(identifier))
    if not external and recovery.get("kind") not in ("upstream", "official-plugin", "bundled", "local-only"):
        raise InstallError("Invalid recovery kind: {}".format(identifier))
    if external and set(recovery) != {"command", "source_url", "note"}:
        raise InstallError("External recovery must contain command, source_url, and note: {}".format(identifier))
    for key in ("command", "source_url"):
        value = recovery.get(key)
        if value is not None:
            display_text(value, "recovery {} for {}".format(key, identifier))
        elif external and key == "source_url":
            raise InstallError("Missing external recovery source_url: {}".format(identifier))
    display_text(recovery.get("note"), "recovery note for " + identifier, allow_empty=True)


def within(path, parent):
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def reject_bundle_symlinks():
    # Check before resolving any manifest-controlled source path. os.walk does
    # not follow links, including links that would otherwise escape the bundle.
    def walk_error(error):
        raise InstallError("Cannot inspect bundle: {}".format(error))

    for directory, directories, files in os.walk(str(BUNDLE), followlinks=False, onerror=walk_error):
        for name in directories + files:
            path = Path(directory) / name
            if path.is_symlink():
                raise InstallError("Bundle contains a forbidden symlink: {}".format(path.relative_to(BUNDLE)))


def load_manifest():
    reject_bundle_symlinks()
    try:
        with (BUNDLE / "manifest.json").open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, ValueError) as error:
        raise InstallError("Cannot read manifest.json: {}".format(error))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise InstallError("manifest.json must have schema_version 1")
    skills = manifest.get("skills")
    if not isinstance(skills, list):
        raise InstallError("manifest.json must contain a skills array")
    seen = set()
    for skill in skills:
        if not isinstance(skill, dict):
            raise InstallError("Each manifest skill must be an object")
        identifier = safe_name(skill.get("id"), "skill id")
        if identifier in seen:
            raise InstallError("Duplicate skill id: {}".format(identifier))
        seen.add(identifier)
        safe_name(skill.get("install_name"), "install_name for " + identifier)
        relative_path(skill.get("path"), "source path for " + identifier)
        display_text(skill.get("name"), "skill name for " + identifier)
        if skill.get("kind") not in ("local", "system", "plugin"):
            raise InstallError("Invalid kind: {}".format(identifier))
        if not isinstance(skill.get("enabled"), bool):
            raise InstallError("Invalid enabled flag: {}".format(identifier))
        files = skill.get("files")
        if not isinstance(files, dict) or "SKILL.md" not in files:
            raise InstallError("Missing files map or SKILL.md: {}".format(identifier))
        for name, metadata in files.items():
            relative_path(name, "file path for " + identifier)
            if not isinstance(metadata, dict):
                raise InstallError("Invalid file metadata: {}/{}".format(identifier, name))
            digest = metadata.get("sha256")
            if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                raise InstallError("Invalid SHA-256: {}/{}".format(identifier, name))
            if not isinstance(metadata.get("executable"), bool):
                raise InstallError("Invalid executable flag: {}/{}".format(identifier, name))
        validate_recovery(skill.get("recovery"), identifier)
    external_skills = manifest.get("external_skills", [])
    if not isinstance(external_skills, list):
        raise InstallError("manifest.json external_skills must be an array")
    external_fields = {"id", "name", "kind", "summary_zh", "plugin_id", "recovery"}
    for skill in external_skills:
        if not isinstance(skill, dict):
            raise InstallError("Each external skill must be an object")
        identifier = safe_name(skill.get("id"), "external skill id")
        if identifier in seen:
            raise InstallError("Duplicate skill id: {}".format(identifier))
        seen.add(identifier)
        if set(skill) - external_fields:
            raise InstallError("Unexpected external skill fields: {}".format(identifier))
        for key in ("name", "summary_zh"):
            display_text(skill.get(key), "external {} for {}".format(key, identifier))
        if skill.get("kind") not in ("system", "plugin"):
            raise InstallError("Invalid external kind: {}".format(identifier))
        if "plugin_id" in skill:
            display_text(skill["plugin_id"], "plugin_id for " + identifier)
        validate_recovery(skill.get("recovery"), identifier, external=True)
    return skills, external_skills


def file_digest(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_tree(root):
    if root.is_symlink() or not root.is_dir():
        raise InstallError("Expected a real directory, not a symlink or file: {}".format(root))
    actual = {}

    def walk_error(error):
        raise InstallError("Cannot inspect skill files: {}".format(error))

    for directory, directories, files in os.walk(str(root), followlinks=False, onerror=walk_error):
        for name in directories:
            path = Path(directory) / name
            if path.is_symlink():
                raise InstallError("Symlink is not allowed: {}".format(path))
        for name in files:
            path = Path(directory) / name
            mode = path.lstat().st_mode
            if not stat.S_ISREG(mode):
                raise InstallError("Only regular files are allowed: {}".format(path))
            actual[path.relative_to(root).as_posix()] = {
                "sha256": file_digest(path),
                "executable": bool(mode & 0o111),
            }
    return actual


def validate_tree(root, expected):
    actual = inspect_tree(root)
    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        parts = []
        if missing:
            parts.append("missing files: " + ", ".join(missing[:5]))
        if extra:
            parts.append("unexpected files: " + ", ".join(extra[:5]))
        raise InstallError("{} ({})".format(root, "; ".join(parts)))
    for name, metadata in expected.items():
        if actual[name]["sha256"] != metadata["sha256"]:
            raise InstallError("SHA-256 mismatch: {}".format(root / name))
        if actual[name]["executable"] != metadata["executable"]:
            raise InstallError("Executable permission mismatch: {}".format(root / name))


def exists(path):
    return os.path.lexists(str(path))


def recovery_message(skill, destination=None, external=False):
    recovery = skill["recovery"]
    if recovery.get("command"):
        kind = "external; install through Codex" if external else recovery["kind"]
        print("  Official/upstream recovery command ({}) [not executed]:".format(kind))
        print("    " + recovery["command"])
    else:
        print("  No verified official installation command is available for this skill.")
    if recovery.get("source_url"):
        print("  Source: " + recovery["source_url"])
    if recovery.get("note"):
        print("  Note: " + recovery["note"])
    if external:
        return
    command = ["bash", str(BUNDLE / "install.sh"), "--skill", skill["id"], "--dest", str(destination)]
    print("  Local retry: " + " ".join(shlex.quote(part) for part in command))


def checked_destination(value):
    destination = Path(value).expanduser().absolute()
    resolved = destination.resolve()
    if within(resolved, BUNDLE) or within(BUNDLE, resolved):
        raise InstallError("Destination and bundle must not overlap: {}".format(destination))
    # A symlink used as the skill-directory container is rejected; individual
    # installed skill symlinks can be backed up with --force without following.
    if destination.is_symlink():
        raise InstallError("Destination directory is a symlink: {}".format(destination))
    if exists(destination) and not destination.is_dir():
        raise InstallError("Destination is not a directory: {}".format(destination))
    # Use the canonical path for subsequent mkdir/rename calls too. This keeps
    # lexical '..' segments from creating incidental directories in the bundle.
    return resolved


def install_one(skill, destination, force=False, dry_run=False):
    source = BUNDLE.joinpath(*relative_path(skill["path"], "source path").parts)
    if not within(source.resolve(), BUNDLE):
        raise InstallError("Source escapes bundle: {}".format(source))
    expected = skill["files"]
    validate_tree(source, expected)
    target = destination / skill["install_name"]
    # If an existing individual skill links into the bundle, moving the link is
    # safe; we deliberately never traverse it for comparison or replacement.
    old_exists = exists(target)
    if old_exists and not target.is_symlink():
        try:
            validate_tree(target, expected)
            return "SKIP", "identical content and executable permissions"
        except (InstallError, OSError):
            pass
    if old_exists and not force:
        raise InstallError("Destination already exists with different files, permissions, or a symlink: {}. Use --force to back it up before replacing.".format(target))
    if dry_run:
        verb = "would back up and replace" if old_exists else "would install"
        return "DRY-RUN", "{} {}".format(verb, target)

    destination.mkdir(parents=True, exist_ok=True)
    # Recheck after mkdir to avoid silently traversing a replaced container.
    checked_destination(str(destination))
    staging = Path(tempfile.mkdtemp(prefix=".codex-skills-stage-", dir=str(destination)))
    backup = None
    moved_old = False
    published = False
    try:
        for relative, metadata in expected.items():
            staged_file = staging.joinpath(*PurePosixPath(relative).parts)
            staged_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(source / relative), str(staged_file))
            staged_file.chmod(0o755 if metadata["executable"] else 0o644)
        validate_tree(staging, expected)

        # A new conflict must never be replaced just because the target was
        # absent when staging began.
        if exists(target):
            if not force:
                raise InstallError("Destination appeared during installation: {}".format(target))
            backup_root = destination.parent / ".codex-skills-backups"
            if backup_root.is_symlink() or (exists(backup_root) and not backup_root.is_dir()):
                raise InstallError("Backup directory must be a real directory: {}".format(backup_root))
            backup_root.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
            backup = backup_root / "{}-{}-{}".format(skill["install_name"], stamp, uuid.uuid4().hex[:8])
            os.rename(str(target), str(backup))
            moved_old = True
        os.rename(str(staging), str(target))
        published = True
        validate_tree(target, expected)
        detail = "installed to {}".format(target)
        if backup is not None:
            detail += "; previous version backed up at {}".format(backup)
        return "OK", detail
    except BaseException as error:
        rollback_error = None
        try:
            if published and exists(target):
                if target.is_symlink() or not target.is_dir():
                    target.unlink()
                else:
                    shutil.rmtree(str(target))
            if moved_old:
                os.rename(str(backup), str(target))
        except OSError as rollback:
            rollback_error = rollback
        if rollback_error is not None:
            raise InstallError("{}; ROLLBACK FAILED: {}. Previous version remains at {}".format(error, rollback_error, backup))
        if moved_old:
            raise InstallError("{}; previous version restored".format(error))
        raise
    finally:
        if exists(staging):
            shutil.rmtree(str(staging))


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", help="Skill directory (default: ${CODEX_HOME:-$HOME/.codex}/skills)")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--skill", action="append", metavar="ID", help="Install a bundled skill or show an external skill's official instructions; repeat to select more")
    selection.add_argument("--all", action="store_true", help="Install all bundled payloads; external skills require installation through Codex")
    parser.add_argument("--list", action="store_true", help="List the inventory without installing (all entries unless explicitly selected)")
    parser.add_argument("--force", action="store_true", help="Back up conflicting destinations, then replace them")
    parser.add_argument("--dry-run", action="store_true", help="Validate and show planned changes without writing anything")
    parser.add_argument("--recovery", metavar="ID", help="Show official/upstream instructions for one skill, with a local retry only for bundled payloads")
    return parser.parse_args()


def main():
    args = parse_arguments()
    try:
        skills, external_skills = load_manifest()
        value = args.dest or str(Path(os.environ.get("CODEX_HOME") or str(Path.home() / ".codex")) / "skills")
        by_id = {skill["id"]: skill for skill in skills + external_skills}
        external_ids = {skill["id"] for skill in external_skills}
        if args.recovery:
            if args.recovery not in by_id:
                raise InstallError("Unknown skill ID: {} (use --list)".format(args.recovery))
            print("Recovery for {}:".format(args.recovery))
            external = args.recovery in external_ids
            destination = None if external else checked_destination(value)
            recovery_message(by_id[args.recovery], destination, external=external)
            return 0
        if args.skill:
            unknown = [identifier for identifier in args.skill if identifier not in by_id]
            if unknown:
                raise InstallError("Unknown skill ID(s): {} (use --list)".format(", ".join(unknown)))
            selected = [by_id[identifier] for identifier in dict.fromkeys(args.skill)]
        elif args.list:
            selected = skills + external_skills
        elif args.all:
            selected = skills
        else:
            selected = [skill for skill in skills if skill["kind"] == "local" and skill["enabled"]]

        if args.list:
            for skill in selected:
                if skill["id"] in external_ids:
                    print("{}\t{}\texternal\tmanual via Codex\t{}".format(skill["id"], skill["kind"], skill["name"]))
                    continue
                default = "default" if skill["enabled"] and skill["kind"] == "local" else "opt-in"
                print("{}\t{}\t{}\t{}\t{}".format(skill["id"], skill["kind"], "enabled" if skill["enabled"] else "disabled", default, skill["name"]))
            external_count = sum(skill["id"] in external_ids for skill in selected)
            print("{} skill(s): {} bundled, {} external. Default installation includes enabled local skills only.".format(len(selected), len(selected) - external_count, external_count))
            return 0
        payloads = [skill for skill in selected if skill["id"] not in external_ids]
        destination = checked_destination(value) if payloads else None
        if args.all and external_skills:
            print("[INFO] {} external skill(s) have no bundled payload and must be installed through Codex. Use --list and --recovery ID for official instructions.".format(len(external_skills)))
        if any(skill["kind"] in ("plugin", "system") for skill in payloads):
            print("[WARN] System/plugin entries are skill-file snapshots only. Copying them does not install plugin tools, MCP servers, credentials, or bundled runtimes; existing system skills may be duplicated.")
        if destination is not None:
            print("Destination: {}".format(destination))
        counts = {"OK": 0, "SKIP": 0, "DRY-RUN": 0, "FAIL": 0, "EXTERNAL": 0}
        installed_names = set()
        for skill in selected:
            if skill["id"] in external_ids:
                counts["EXTERNAL"] += 1
                print("[EXTERNAL] {}: no bundled payload; install through Codex using the official instructions below.".format(skill["id"]))
                recovery_message(skill, external=True)
                continue
            try:
                if skill["install_name"] in installed_names:
                    raise InstallError("Another selected skill uses the same destination directory: {}".format(skill["install_name"]))
                installed_names.add(skill["install_name"])
                status, detail = install_one(skill, destination, args.force, args.dry_run)
                counts[status] += 1
                print("[{}] {}: {}".format(status, skill["id"], detail))
            except (InstallError, OSError, ValueError) as error:
                counts["FAIL"] += 1
                print("[FAIL] {}: {}".format(skill["id"], error))
                recovery_message(skill, destination)
        print("Summary: {} installed, {} identical/skipped, {} planned, {} failed, {} external instructions shown (not installed).".format(counts["OK"], counts["SKIP"], counts["DRY-RUN"], counts["FAIL"], counts["EXTERNAL"]))
        if counts["OK"]:
            print("Start a new Codex conversation to load newly installed skills.")
        return 1 if counts["FAIL"] else 0
    except (InstallError, OSError, ValueError) as error:
        print("[FAIL] Installer setup: {}".format(error), file=sys.stderr)
        print("No installation was attempted. Check manifest.json and the bundle, or use the recovery information in readme.md.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
