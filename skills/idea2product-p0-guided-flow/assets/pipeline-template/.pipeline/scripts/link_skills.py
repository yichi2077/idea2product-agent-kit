from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACTIVE = ROOT / ".agents" / "skills"
SOURCES = [
    ROOT / ".pipeline" / "vendor" / "strategy",
    ROOT / ".pipeline" / "vendor" / "product",
    ROOT / ".pipeline" / "vendor" / "engineering",
    ROOT / ".pipeline" / "custom-skills",
]
EXCLUDED = {"superpowers-codex-tools-reference"}


def safe_remove(path: Path) -> None:
    active_root = ACTIVE.absolute()
    target = path.absolute()
    if active_root not in [target, *target.parents]:
        raise RuntimeError(f"Refusing to remove outside active skills: {path}")
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        if os.name == "nt":
            try:
                subprocess.check_call(["cmd", "/c", "rmdir", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                pass
        shutil.rmtree(path)


def link_or_copy(src: Path, dst: Path) -> str:
    if dst.exists() or dst.is_symlink():
        safe_remove(dst)
    if os.name == "nt":
        try:
            subprocess.check_call(["cmd", "/c", "mklink", "/J", str(dst), str(src)], stdout=subprocess.DEVNULL)
            return "junction"
        except Exception:
            pass
    try:
        dst.symlink_to(src, target_is_directory=True)
        return "symlink"
    except Exception:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        return "copy"


def iter_skills() -> list[Path]:
    skills: list[Path] = []
    for source in SOURCES:
        if not source.exists():
            continue
        for child in sorted(source.iterdir()):
            if child.name in EXCLUDED:
                continue
            if (child / "SKILL.md").exists():
                skills.append(child)
    return skills


def main() -> int:
    ACTIVE.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    for src in iter_skills():
        if src.name in seen:
            print(f"Duplicate skill name: {src.name}", file=sys.stderr)
            return 1
        seen.add(src.name)
        mode = link_or_copy(src, ACTIVE / src.name)
        print(f"{src.name}: {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
