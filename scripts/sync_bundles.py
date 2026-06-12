#!/usr/bin/env python3
"""Keep the duplicated copies in this kit byte-identical to their canonical source.

There are two canonical sources and two levels of duplication:

  1. ``pipeline-template/``  is the single source for the scaffolded workspace.
     It is embedded inside the guided-flow skill as ``assets/pipeline-template``.

  2. ``skills/``  (the 12 entry skills) is the single source for the skills the
     user installs. The Hermes and OpenClaw adapters embed a full copy under
     ``agent-adapters/<host>/skills``.

Mirror order matters: the template is copied into the guided-flow skill first, so
that when ``skills/`` is mirrored into the adapters the refreshed assets ride along.

Usage:
    python scripts/sync_bundles.py          # copy canonical -> all mirrors
    python scripts/sync_bundles.py --check  # exit non-zero if any mirror drifts
"""
from __future__ import annotations

import argparse
import filecmp
import sys
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]

# (source, destination) pairs, processed in order. Earlier pairs feed later ones.
MIRRORS: list[tuple[Path, Path]] = [
    (
        KIT_ROOT / "pipeline-template",
        KIT_ROOT / "skills/idea2product-p0-guided-flow/assets/pipeline-template",
    ),
    (KIT_ROOT / "skills", KIT_ROOT / "agent-adapters/hermes/skills"),
    (KIT_ROOT / "skills", KIT_ROOT / "agent-adapters/openclaw/skills"),
]
PRUNE_NAMES = {"__pycache__", ".pytest_cache", ".git", ".venv"}


def iter_files(base: Path) -> set[Path]:
    files: set[Path] = set()
    if not base.exists():
        return files
    for path in base.rglob("*"):
        rel = path.relative_to(base)
        if any(part in PRUNE_NAMES for part in rel.parts):
            continue
        if path.suffix == ".pyc":
            continue
        if path.is_file():
            files.add(rel)
    return files


def diff(source: Path, dest: Path) -> list[str]:
    problems: list[str] = []
    src_files = iter_files(source)
    dst_files = iter_files(dest)
    for rel in sorted(src_files - dst_files):
        problems.append(f"missing in mirror: {rel}")
    for rel in sorted(dst_files - src_files):
        problems.append(f"extra in mirror: {rel}")
    for rel in sorted(src_files & dst_files):
        if not filecmp.cmp(source / rel, dest / rel, shallow=False):
            problems.append(f"content differs: {rel}")
    return problems


def mirror(source: Path, dest: Path) -> None:
    import shutil

    src_files = iter_files(source)
    dest.mkdir(parents=True, exist_ok=True)
    dst_files = iter_files(dest)
    for rel in sorted(src_files):
        src, dst = source / rel, dest / rel
        if dst.exists() and filecmp.cmp(src, dst, shallow=False):
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    for rel in sorted(dst_files - src_files):
        (dest / rel).unlink()
    for path in sorted(dest.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def check() -> int:
    drift = False
    for source, dest in MIRRORS:
        problems = diff(source, dest)
        label = dest.relative_to(KIT_ROOT)
        if problems:
            drift = True
            print(f"DRIFT in {label}:")
            for problem in problems[:20]:
                print(f"  - {problem}")
            if len(problems) > 20:
                print(f"  ... and {len(problems) - 20} more")
        else:
            print(f"in sync: {label}")
    if drift:
        print("\nRun: python scripts/sync_bundles.py", file=sys.stderr)
        return 1
    print("All mirrors are in sync with their canonical sources.")
    return 0


def sync() -> int:
    for source, dest in MIRRORS:
        if not source.exists():
            print(f"Canonical source not found: {source}", file=sys.stderr)
            return 2
        mirror(source, dest)
        print(f"synced: {dest.relative_to(KIT_ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report drift without copying")
    args = parser.parse_args()
    return check() if args.check else sync()


if __name__ == "__main__":
    raise SystemExit(main())
