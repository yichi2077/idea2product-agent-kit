#!/usr/bin/env python3
"""Keep the bundled (derived) copies of the kit in sync with their canonical sources.

The kit intentionally ships several byte-identical copies of the same content so
that each distribution path is self-contained:

  Canonical source                         Derived copy (must match the source)
  ---------------------------------------  ----------------------------------------------------
  pipeline-template/                   ->  skills/idea2product-p0-guided-flow/assets/pipeline-template/
  skills/                              ->  agent-adapters/hermes/skills/
  skills/                              ->  agent-adapters/openclaw/skills/

`skills/idea2product-p0-guided-flow/assets/pipeline-template/` lets the guided-flow
skill scaffold a workspace when only the skills were installed. The hermes/openclaw
adapters need full local skill copies because those hosts register skills from their
own directory. Host-specific files (AGENTS.md, SOUL.md, openai.yaml policy, ...) live
at the *adapter root*, not inside the skill dirs, so a full mirror is safe.

Editing a canonical file therefore means the derived copies drift until you re-run
this script. Use it as the single sync point:

  python3 scripts/sync_bundled_copies.py            # --check (default): report drift, exit 1 if any
  python3 scripts/sync_bundled_copies.py --write     # regenerate every derived copy from canonical
  python3 scripts/sync_bundled_copies.py --check      # explicit check (CI-friendly)

Pure stdlib; same Python the rest of the kit already requires.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
# Mirror .gitignore: only TRACKED content is canonical. In particular .agents/ holds
# absolute symlinks generated per-machine by link_skills.py; copying it would
# dereference those into real files and corrupt the bundle, so it is never synced.
IGNORE_NAMES = {
    "__pycache__", ".pytest_cache", ".DS_Store",
    ".agents", ".venv", "node_modules", ".claude",
}
IGNORE_SUFFIXES = {".pyc"}

# Order matters for --write: refresh the bundled pipeline-template that lives *inside*
# skills/ before mirroring skills/ into the host adapters, so the refreshed bundle
# propagates in the same run.
PAIRS: list[tuple[Path, Path]] = [
    (
        KIT_ROOT / "pipeline-template",
        KIT_ROOT / "skills" / "idea2product-p0-guided-flow" / "assets" / "pipeline-template",
    ),
    (KIT_ROOT / "skills", KIT_ROOT / "agent-adapters" / "hermes" / "skills"),
    (KIT_ROOT / "skills", KIT_ROOT / "agent-adapters" / "openclaw" / "skills"),
]


def is_ignored(path: Path) -> bool:
    return path.name in IGNORE_NAMES or path.suffix in IGNORE_SUFFIXES


def relevant_files(root: Path) -> dict[str, Path]:
    """Map each tracked file to its path, relative to *root*, skipping ignored names."""
    files: dict[str, Path] = {}
    if not root.exists():
        return files
    for path in root.rglob("*"):
        if any(part in IGNORE_NAMES for part in path.relative_to(root).parts):
            continue
        if path.is_file() and not is_ignored(path):
            files[str(path.relative_to(root))] = path
    return files


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def diff_pair(source: Path, derived: Path) -> list[str]:
    src_files = relevant_files(source)
    dst_files = relevant_files(derived)
    problems: list[str] = []
    for rel in sorted(set(src_files) - set(dst_files)):
        problems.append(f"missing in derived: {derived.relative_to(KIT_ROOT)}/{rel}")
    for rel in sorted(set(dst_files) - set(src_files)):
        problems.append(f"stale in derived (no canonical source): {derived.relative_to(KIT_ROOT)}/{rel}")
    for rel in sorted(set(src_files) & set(dst_files)):
        if sha256(src_files[rel]) != sha256(dst_files[rel]):
            problems.append(f"content differs: {derived.relative_to(KIT_ROOT)}/{rel}")
    return problems


def regenerate(source: Path, derived: Path) -> None:
    if not source.exists():
        raise SystemExit(f"canonical source does not exist: {source}")
    if derived.exists():
        shutil.rmtree(derived)
    derived.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        derived,
        ignore=shutil.ignore_patterns(*IGNORE_NAMES, "*.pyc"),
        symlinks=True,  # preserve any symlink as a symlink; never dereference into real files
    )


def cmd_check() -> int:
    all_problems: list[str] = []
    for source, derived in PAIRS:
        all_problems.extend(diff_pair(source, derived))
    if all_problems:
        print("Bundled copies are OUT OF SYNC with canonical sources:")
        for problem in all_problems:
            print(f"- {problem}")
        print("\nRun: python3 scripts/sync_bundled_copies.py --write")
        return 1
    print("✓ All bundled copies are in sync with their canonical sources.")
    return 0


def cmd_write() -> int:
    for source, derived in PAIRS:
        regenerate(source, derived)
        print(f"Synced: {source.relative_to(KIT_ROOT)} -> {derived.relative_to(KIT_ROOT)}")
    # Confirm the result is actually clean (catches copy bugs early).
    return cmd_check()


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="sync_bundled_copies.py",
        description="Sync the kit's derived copies with their canonical sources.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="report drift; exit 1 if any (default)")
    group.add_argument("--write", action="store_true", help="regenerate derived copies from canonical")
    args = parser.parse_args()
    return cmd_write() if args.write else cmd_check()


if __name__ == "__main__":
    raise SystemExit(main())
