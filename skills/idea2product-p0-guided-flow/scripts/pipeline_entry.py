from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_ROOT / "assets" / "pipeline-template"


def find_root(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".pipeline/scripts/pipeline.py").exists():
            return candidate
    return None


def run_pipeline(args: list[str]) -> int:
    no_auto_init = "--no-auto-init" in args
    args = [arg for arg in args if arg != "--no-auto-init"]
    root = find_root(Path.cwd())
    if root is None:
        if no_auto_init:
            print("No .pipeline/scripts/pipeline.py found from the current directory upward.", file=sys.stderr)
            print("Initialize this workspace with:", file=sys.stderr)
            print(f"  {sys.executable} {Path(__file__).resolve()} init .", file=sys.stderr)
            return 2
        print("No .pipeline/scripts/pipeline.py found; initializing idea2product in the current workspace.", file=sys.stderr)
        init_code = init_workspace(Path.cwd(), force=False, verify=False)
        if init_code != 0:
            return init_code
        root = find_root(Path.cwd())
        if root is None:
            print("Initialization completed but .pipeline/scripts/pipeline.py is still missing.", file=sys.stderr)
            return 2
    cmd = [sys.executable, str(root / ".pipeline/scripts/pipeline.py"), *args]
    return subprocess.call(cmd, cwd=root)


def copy_path(src: Path, dst: Path, force: bool) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    if dst.exists():
        if force:
            if dst.is_file():
                dst.unlink()
            else:
                shutil.rmtree(dst)
        elif src.is_dir() and dst.is_dir():
            for child in src.iterdir():
                copy_path(child, dst / child.name, force=False)
            return
        elif dst.name == "AGENTS.md":
            sidecar = dst.with_name("AGENTS.idea2product.md")
            shutil.copy2(src, sidecar)
            print(f"Preserved existing {dst.name}; wrote {sidecar.name} instead.")
            return
        else:
            print(f"Preserved existing {dst}; skipped bundled {src.name}.")
            return
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    else:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))


def init_workspace(target: Path, force: bool, verify: bool) -> int:
    if not TEMPLATE.exists():
        print(f"Bundled pipeline template not found: {TEMPLATE}", file=sys.stderr)
        return 2
    target = target.resolve()
    target.mkdir(parents=True, exist_ok=True)
    for name in [".pipeline", "docs", ".github", "AGENTS.md"]:
        copy_path(TEMPLATE / name, target / name, force)
    link = target / ".pipeline" / "scripts" / "link_skills.py"
    if link.exists():
        subprocess.check_call([sys.executable, str(link)], cwd=target)
    if verify:
        # Opt-in developer check; requires pytest + PyYAML. Not run on the
        # end-user auto-init path so first use never depends on a test runner.
        scripts = target / ".pipeline" / "scripts"
        if sys.platform.startswith("win"):
            verify_script = scripts / "verify.ps1"
            cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(verify_script)]
        else:
            verify_script = scripts / "verify.sh"
            cmd = ["sh", str(verify_script)]
        if verify_script.exists():
            subprocess.check_call(cmd, cwd=target)
    print(f"Initialized idea2product pipeline in {target}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="pipeline-entry")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parsed = parser.parse_args()
    if not parsed.args:
        parsed.args = ["status"]
    if parsed.args[0] in {"init", "scaffold"}:
        target = Path(parsed.args[1]) if len(parsed.args) > 1 and not parsed.args[1].startswith("-") else Path.cwd()
        force = "--force" in parsed.args
        verify = "--verify" in parsed.args  # opt-in; off by default for end users
        return init_workspace(target, force=force, verify=verify)
    return run_pipeline(parsed.args)


if __name__ == "__main__":
    raise SystemExit(main())
