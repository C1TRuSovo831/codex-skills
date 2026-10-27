#!/usr/bin/env python3
"""Download pinned research skills with Codex's installer; never run their code."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

import install


REPO = Path(__file__).resolve().parents[1]
LOCK = REPO / "provenance/research-skills-lock.json"
RECEIPT = ".installation-provenance.json"
SKILL_IDS = {"ai-research-writing-skill", "citation-management", "peer-review"}


def load_sources():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if not isinstance(lock, dict) or lock.get("schema_version") != 1:
        raise install.InstallError("Unsupported research download lock")
    sources = lock.get("skills")
    if not isinstance(sources, list) or len(sources) != len(SKILL_IDS):
        raise install.InstallError("Lock must contain exactly the three research skills")
    seen = set()
    for source in sources:
        if not isinstance(source, dict):
            raise install.InstallError("Invalid download source")
        name = install.safe_name(source.get("id"), "download skill id")
        if name not in SKILL_IDS or name in seen:
            raise install.InstallError("Unexpected or duplicate research skill: " + name)
        seen.add(name)
        if not isinstance(source.get("repo"), str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", source["repo"]):
            raise install.InstallError("Invalid GitHub repository: " + name)
        if not isinstance(source.get("ref"), str) or not re.fullmatch(r"[0-9a-f]{40}", source["ref"]):
            raise install.InstallError("Download must use a full Git commit: " + name)
        if source.get("path") != ".":
            install.relative_path(source.get("path"), "download source path")
        if source.get("method") not in {"download", "git"}:
            raise install.InstallError("Invalid download method: " + name)
        if source["path"] == "." and source["method"] != "download":
            raise install.InstallError("Root skills require archive download, excluding .git")
        files = source.get("files")
        if not isinstance(files, dict) or "SKILL.md" not in files or RECEIPT in files:
            raise install.InstallError("Invalid downloaded file inventory: " + name)
        for relative, metadata in files.items():
            install.relative_path(relative, "download file path")
            if not isinstance(metadata, dict) or not isinstance(metadata.get("sha256"), str) or not install.SHA256.fullmatch(metadata["sha256"]):
                raise install.InstallError("Invalid file digest: " + relative)
            if not isinstance(metadata.get("executable"), bool):
                raise install.InstallError("Invalid executable flag: " + relative)
    return sources


def receipt_bytes(source):
    receipt = {"schema_version": 1, "repo": source["repo"], "commit": source["ref"],
               "source_path": source["path"], "name": source["id"],
               "files": source["files"], "runtime_verification": "NOT_RUN"}
    return (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")


def install_record(source):
    files = dict(source["files"])
    files[RECEIPT] = {"sha256": hashlib.sha256(receipt_bytes(source)).hexdigest(), "executable": False}
    return {"id": source["id"], "install_name": source["id"], "path": source["id"], "files": files}


def existing_status(source, destination):
    target = destination / source["id"]
    if not install.exists(target):
        return "NEW"
    try:
        install.validate_tree(target, install_record(source)["files"])
        return "IDENTICAL"
    except (install.InstallError, OSError):
        pass
    # Also recognize the provenance receipt produced by the initial Codex install.
    # Its timestamps differ; every payload byte and executable bit must still match.
    try:
        actual = install.inspect_tree(target)
        receipt = target / RECEIPT
        if receipt.stat().st_size <= 256 * 1024:
            old = json.loads(receipt.read_text(encoding="utf-8"))
            if isinstance(old, dict) and (old.get("repo"), old.get("commit"), old.get("name")) == (source["repo"], source["ref"], source["id"]):
                actual.pop(RECEIPT, None)
                if actual == source["files"]:
                    return "IDENTICAL"
    except (install.InstallError, OSError, ValueError):
        pass
    return "CONFLICT"


def codex_installer():
    home = Path(os.environ.get("CODEX_HOME") or str(Path.home() / ".codex"))
    candidates = [home / "skills/.system/skill-installer/scripts/install-skill-from-github.py",
                  REPO / "bundled/system/skill-installer/scripts/install-skill-from-github.py"]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise install.InstallError("Codex skill-installer is unavailable")


def download_sources(sources, directory, installer):
    groups = {}
    for source in sources:
        groups.setdefault((source["repo"], source["ref"], source["method"]), []).append(source)
    for (repo, ref, method), members in groups.items():
        command = [sys.executable, "-B", str(installer), "--repo", repo, "--ref", ref,
                   "--method", method, "--dest", str(directory), "--path"]
        command.extend(source["path"] for source in members)
        if len(members) == 1:
            command.extend(["--name", members[0]["id"]])
        print("[DOWNLOAD] {} @ {} ({})".format(repo, ref, method), flush=True)
        # Only the trusted Codex installer is executed, never downloaded code.
        try:
            subprocess.run(command, check=True, timeout=600)
        except subprocess.CalledProcessError:
            # Some Codex installer versions shallow-clone only the default branch,
            # so an older pinned SHA cannot be checked out. Keep the same commit
            # and download only its locked files instead of following main.
            if method != "git" or any(install.exists(directory / s["id"]) for s in members):
                raise
            print("[FALLBACK] Fetching locked files over HTTPS at the same commit.", flush=True)
            download_locked_files(members, directory)


def download_locked_files(sources, directory):
    def fetch(item):
        source, relative = item
        path = relative if source["path"] == "." else source["path"] + "/" + relative
        url = "https://raw.githubusercontent.com/{}/{}/{}".format(
            source["repo"], source["ref"], urllib.parse.quote(path, safe="/"))
        request = urllib.request.Request(url, headers={"User-Agent": "codex-skills-research-downloader/1"})
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read()
        if hashlib.sha256(content).hexdigest() != source["files"][relative]["sha256"]:
            raise install.InstallError("Downloaded file SHA-256 mismatch: " + source["id"] + "/" + relative)
        target = directory / source["id"] / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    files = [(source, relative) for source in sources for relative in source["files"]]
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(fetch, files))


def prepare(source, downloaded, prepared):
    root = downloaded / source["id"]
    # Reject symlinks even among excluded files before copying any source data.
    install.inspect_tree(root)
    manifest = (root / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = manifest.split("---", 2)
    if len(frontmatter) != 3 or frontmatter[0].strip() or not re.search(
            r"^name:\s*" + re.escape(source["id"]) + r"\s*$", frontmatter[1], re.MULTILINE):
        raise install.InstallError("Downloaded SKILL.md has the wrong name: " + source["id"])
    target = prepared / source["id"]
    target.mkdir()
    for relative, metadata in source["files"].items():
        origin = root / relative
        if not origin.is_file() or install.file_digest(origin) != metadata["sha256"]:
            raise install.InstallError("Downloaded file missing or SHA-256 mismatch: " + source["id"] + "/" + relative)
        output = target / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(origin), str(output))
        output.chmod(0o755 if metadata["executable"] else 0o644)
    receipt = target / RECEIPT
    receipt.write_bytes(receipt_bytes(source))
    receipt.chmod(0o644)
    install.validate_tree(target, install_record(source)["files"])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", choices=sorted(SKILL_IDS), help="Select a skill; repeat as needed (default: all three)")
    parser.add_argument("--dest", help="Codex skills directory; honors CODEX_HOME by default")
    parser.add_argument("--list", action="store_true", help="Show pinned sources without downloading")
    parser.add_argument("--dry-run", action="store_true", help="Check local state and show the plan without network or writes")
    parser.add_argument("--force", action="store_true", help="Back up conflicting skill directories before replacement")
    args = parser.parse_args(argv)
    try:
        sources = [s for s in load_sources() if not args.skill or s["id"] in args.skill]
        for source in sources:
            print("{}: https://github.com/{} @ {} path={} ({} files)".format(source["id"], source["repo"], source["ref"], source["path"], len(source["files"])))
        if args.list:
            return 0
        destination = install.checked_destination(args.dest or str(Path(os.environ.get("CODEX_HOME") or str(Path.home() / ".codex")) / "skills"))
        pending = []
        conflicts = []
        for source in sources:
            state = existing_status(source, destination)
            print("[{}] {}".format(state, destination / source["id"]))
            if state == "CONFLICT" and not args.force:
                conflicts.append(source["id"])
            if state != "IDENTICAL":
                pending.append(source)
        if conflicts:
            raise install.InstallError("Existing skills preserved: {}. Inspect their provenance first; --force explicitly backs up before replacing.".format(", ".join(conflicts)))
        if args.dry_run or not pending:
            print("No network or installation performed.")
            return 0
        installer = codex_installer()
        print("Codex installer: " + str(installer))
        print("[NOTE] File installation only; no dependency installation or skill execution.")
        if any(s["id"] == "ai-research-writing-skill" for s in pending):
            print("[NOTE] Upstream verify_citations.py records OpenAlex keys in URLs; repair before using its keyed branch. See readme.md.")
        with tempfile.TemporaryDirectory(prefix="codex-research-download-") as scratch:
            scratch = Path(scratch)
            downloaded, prepared = scratch / "downloaded", scratch / "prepared"
            prepared.mkdir()
            download_sources(pending, downloaded, installer)
            # Verify the complete selected batch before publishing any skill.
            for source in pending:
                prepare(source, downloaded, prepared)
            previous_bundle = install.BUNDLE
            try:
                install.BUNDLE = prepared
                for source in pending:
                    status, detail = install.install_one(install_record(source), destination, force=args.force)
                    print("[{}] {}: {}".format(status, source["id"], detail))
            finally:
                install.BUNDLE = previous_bundle
        print("Files installed and verified. Runtime functionality was not tested. Available on the next Codex turn.")
        return 0
    except (install.InstallError, OSError, ValueError, subprocess.SubprocessError) as error:
        print("[FAIL] " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
