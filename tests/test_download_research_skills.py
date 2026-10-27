"""Offline downloader tests with synthetic sources; downloaded code is never run.

Scratch fixtures are marked REMOVABLE and retained for explicit cleanup approval.
Set CODEX_SKILLS_TEST_ARTIFACTS to place them under a chosen scratch directory.
"""

import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import download_research_skills as downloader
sys.path.pop(0)


class ResearchDownloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = os.environ.get("CODEX_SKILLS_TEST_ARTIFACTS")
        if parent:
            Path(parent).mkdir(parents=True, exist_ok=True)
        cls.artifacts = Path(tempfile.mkdtemp(prefix="research-download-tests-", dir=parent))
        (cls.artifacts / "REMOVABLE.txt").write_text(
            "Synthetic test artifacts; retain until the user explicitly approves deletion.\n")

    @classmethod
    def tearDownClass(cls):
        print("\nResearch download test artifacts retained: " + str(cls.artifacts))

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix=self._testMethodName + "-", dir=str(self.artifacts)))
        self.destination = self.root / "skills with spaces"
        self.fixture = self.root / "download fixture"
        self.lock = json.loads((REPO / "provenance/research-skills-lock.json").read_text())
        self.executed = self.root / "skill code executed"
        for source in self.lock["skills"]:
            root = self.fixture / source["id"]
            payload = {
                "SKILL.md": "---\nname: {}\ndescription: Synthetic test skill.\n---\n".format(source["id"]),
                "references/guide.md": "Synthetic reference.\n",
                "scripts/do_not_run.py": "from pathlib import Path\nPath({!r}).touch()\n".format(str(self.executed)),
            }
            source["files"] = {}
            for relative, content in payload.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                source["files"][relative] = {"sha256": hashlib.sha256(content.encode()).hexdigest(), "executable": relative.endswith(".py")}
            (root / "unrelated-example.md").write_text("Must not be installed.\n")
        self.lock_path = self.root / "lock.json"
        self.save_lock()

    def save_lock(self):
        self.lock_path.write_text(json.dumps(self.lock))

    def fake_download(self, sources, directory, installer):
        directory.mkdir()
        for source in sources:
            shutil.copytree(self.fixture / source["id"], directory / source["id"])

    def run_download(self, *args, download=None):
        output = io.StringIO()
        with mock.patch.object(downloader, "LOCK", self.lock_path), \
                mock.patch.object(downloader, "download_sources", side_effect=download or self.fake_download) as network, \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = downloader.main(["--dest", str(self.destination), *args])
        return result, output.getvalue(), network

    def test_download_installs_only_locked_files_and_records_commit_without_execution(self):
        result, output, network = self.run_download()
        self.assertEqual(result, 0, output)
        self.assertEqual(network.call_count, 1)
        self.assertEqual({p.name for p in self.destination.iterdir()}, downloader.SKILL_IDS)
        for source in self.lock["skills"]:
            root = self.destination / source["id"]
            downloader.install.validate_tree(root, downloader.install_record(source)["files"])
            receipt = json.loads((root / downloader.RECEIPT).read_text())
            self.assertEqual(receipt["commit"], source["ref"])
            self.assertEqual(receipt["runtime_verification"], "NOT_RUN")
        self.assertFalse(self.executed.exists())

    def test_repeat_install_skips_network_and_preserves_file_timestamps(self):
        self.assertEqual(self.run_download()[0], 0)
        before = {p: p.stat().st_mtime_ns for p in self.destination.rglob("*")}
        result, output, network = self.run_download()
        self.assertEqual(result, 0, output)
        network.assert_not_called()
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in self.destination.rglob("*")})

    def test_initial_codex_receipt_is_recognized_only_when_payload_matches(self):
        self.assertEqual(self.run_download()[0], 0)
        source = self.lock["skills"][0]
        receipt = self.destination / source["id"] / downloader.RECEIPT
        receipt.write_text(json.dumps({"name": source["id"], "repo": source["repo"], "commit": source["ref"], "installed_at": "historical timestamp"}))
        result, output, network = self.run_download()
        self.assertEqual(result, 0, output)
        network.assert_not_called()
        (receipt.parent / "SKILL.md").write_text("local changes")
        result, output, network = self.run_download()
        self.assertEqual(result, 1, output)
        network.assert_not_called()
        self.assertEqual((receipt.parent / "SKILL.md").read_text(), "local changes")

    def test_conflict_is_reported_before_network_and_force_preserves_backup(self):
        source = self.lock["skills"][0]
        target = self.destination / source["id"]
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("previous local content")
        result, output, network = self.run_download("--skill", source["id"])
        self.assertEqual(result, 1, output)
        network.assert_not_called()
        self.assertEqual((target / "SKILL.md").read_text(), "previous local content")
        result, output, network = self.run_download("--skill", source["id"], "--force")
        self.assertEqual(result, 0, output)
        backups = list((self.destination.parent / ".codex-skills-backups").iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "SKILL.md").read_text(), "previous local content")

    def test_list_and_dry_run_do_not_download_or_create_destination(self):
        for flag in ("--list", "--dry-run"):
            result, output, network = self.run_download(flag)
            self.assertEqual(result, 0, output)
            network.assert_not_called()
            self.assertFalse(self.destination.exists())

    def test_selection_downloads_only_requested_skill(self):
        result, output, network = self.run_download("--skill", "citation-management")
        self.assertEqual(result, 0, output)
        self.assertEqual([s["id"] for s in network.call_args[0][0]], ["citation-management"])
        self.assertEqual([p.name for p in self.destination.iterdir()], ["citation-management"])

    def test_corrupt_late_source_prevents_entire_batch_publication(self):
        source = self.lock["skills"][-1]
        (self.fixture / source["id"] / "references/guide.md").write_text("tampered")
        result, output, network = self.run_download()
        self.assertEqual(result, 1, output)
        self.assertIn("SHA-256 mismatch", output)
        self.assertFalse(self.destination.exists())

    def test_wrong_skill_name_is_rejected_even_with_matching_digest(self):
        source = self.lock["skills"][0]
        path = self.fixture / source["id"] / "SKILL.md"
        path.write_text("---\nname: wrong\ndescription: synthetic\n---\n")
        source["files"]["SKILL.md"]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.save_lock()
        result, output, network = self.run_download()
        self.assertEqual(result, 1, output)
        self.assertIn("wrong name", output)
        self.assertFalse(self.destination.exists())

    def test_network_failure_leaves_destination_untouched(self):
        result, output, network = self.run_download(download=mock.Mock(side_effect=OSError("simulated download failure")))
        self.assertEqual(result, 1, output)
        self.assertIn("simulated download failure", output)
        self.assertFalse(self.destination.exists())

    def test_symlink_destination_is_not_followed(self):
        other = self.root / "untouched"
        other.mkdir()
        self.destination.symlink_to(other, target_is_directory=True)
        result, output, network = self.run_download("--force")
        self.assertEqual(result, 1, output)
        network.assert_not_called()
        self.assertEqual(list(other.iterdir()), [])

    def test_unsafe_paths_or_unpinned_refs_fail_before_network(self):
        original = copy.deepcopy(self.lock)
        for field, value in (("path", "../escape"), ("ref", "main"), ("repo", "https://unexpected.example/repo")):
            with self.subTest(field=field):
                self.lock = copy.deepcopy(original)
                self.lock["skills"][0][field] = value
                self.save_lock()
                result, output, network = self.run_download()
                self.assertEqual(result, 1, output)
                network.assert_not_called()
                self.assertFalse(self.destination.exists())

    def test_codex_installer_receives_pinned_grouped_arguments(self):
        destination = self.root / "source downloads"
        installer = self.root / "Codex helper.py"
        with mock.patch.object(downloader.subprocess, "run") as run:
            downloader.download_sources(self.lock["skills"], destination, installer)
        self.assertEqual(run.call_count, 2)
        ai, kdense = [call.args[0] for call in run.call_args_list]
        self.assertIn(self.lock["skills"][0]["ref"], ai)
        self.assertEqual(ai[-2:], ["--name", "ai-research-writing-skill"])
        self.assertIn("download", ai)
        self.assertIn(self.lock["skills"][1]["ref"], kdense)
        self.assertIn("git", kdense)
        self.assertEqual(kdense[-3:], ["--path", "skills/citation-management", "skills/peer-review"])

    def test_git_failure_falls_back_to_only_locked_files_at_the_same_commit(self):
        sources = self.lock["skills"][1:]
        destination = self.root / "fallback downloads"
        expected = {}
        for source in sources:
            for relative in source["files"]:
                url = "https://raw.githubusercontent.com/{}/{}/{}/{}".format(source["repo"], source["ref"], source["path"], relative)
                expected[url] = (self.fixture / source["id"] / relative).read_bytes()
        seen = []

        def response(request, timeout):
            seen.append(request.full_url)
            return io.BytesIO(expected[request.full_url])

        with mock.patch.object(downloader.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "Codex installer")), \
                mock.patch.object(downloader.urllib.request, "urlopen", side_effect=response):
            downloader.download_sources(sources, destination, self.root / "helper.py")
        self.assertEqual(set(seen), set(expected))
        prepared = self.root / "fallback prepared"
        prepared.mkdir()
        for source in sources:
            downloader.prepare(source, destination, prepared)
            downloader.install.validate_tree(prepared / source["id"], downloader.install_record(source)["files"])
        self.assertFalse(self.executed.exists())

    def test_archive_failure_does_not_change_transport_or_revision(self):
        with mock.patch.object(downloader.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "Codex installer")), \
                mock.patch.object(downloader.urllib.request, "urlopen") as network:
            with self.assertRaises(subprocess.CalledProcessError):
                downloader.download_sources(self.lock["skills"][:1], self.root / "failed archive", self.root / "helper.py")
        network.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
