#!/usr/bin/env python3
"""Cross-platform installer for the idea2product Agent Kit.

Works the same on Windows, macOS, and Linux. Python is the only requirement
(the same Python the pipeline already needs) -- no PowerShell, no bash.

Subcommands:
  skills              Install the 12 entry skills into the user's agent skill dir(s).
  scaffold <repo>     Create the .pipeline engine + docs inside a target repository.
  adapters <repo>     Install host adapter files into a target repository.

Examples:
  python3 scripts/install.py skills --target claude-code  # macOS/Linux
  python scripts/install.py skills --target claude-code   # Windows
  python3 scripts/install.py skills                       # both claude-code and codex
  python3 scripts/install.py scaffold /path/to/repo
  python3 scripts/install.py adapters /path/to/repo --agent all
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
SKILLS_SRC = KIT_ROOT / "skills"
TEMPLATE = KIT_ROOT / "pipeline-template"
ADAPTERS = KIT_ROOT / "agent-adapters"
HOME = Path.home()
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")


def copy_skill_dirs(source: Path, dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    count = 0
    for child in sorted(source.iterdir()):
        if not child.is_dir():
            continue
        target = dest / child.name
        backup_if_exists(target)
        shutil.copytree(child, target, ignore=IGNORE)
        count += 1
    return count


def backup_if_exists(path: Path) -> None:
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = path.with_name(f"{path.name}.bak-{stamp}")
        suffix = 1
        while backup.exists():
            backup = path.with_name(f"{path.name}.bak-{stamp}-{suffix}")
            suffix += 1
        path.rename(backup)
        print(f"Backed up {path.name} -> {backup.name}")


def copy_tree(src: Path, dst: Path) -> None:
    backup_if_exists(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, ignore=IGNORE)
    print(f"Installed: {dst}")


def copy_file(src: Path, dst: Path) -> None:
    backup_if_exists(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"Installed: {dst}")


# ---------------------------------------------------------------- skills

def cmd_skills(args: argparse.Namespace) -> int:
    destinations: list[Path] = []
    if args.target in ("both", "codex"):
        destinations.append(HOME / ".agents" / "skills")       # Codex / AgentSkills
    if args.target in ("both", "claude-code"):
        destinations.append(HOME / ".claude" / "skills")       # Claude Code personal
    for dest in destinations:
        n = copy_skill_dirs(SKILLS_SRC, dest)
        print(f"Installed {n} idea2product skills to {dest}")
    print("Restart the agent or open a new thread if the skills do not appear immediately.")
    return 0


# ---------------------------------------------------------------- scaffold

def cmd_scaffold(args: argparse.Namespace) -> int:
    target = Path(args.repo).resolve()
    target.mkdir(parents=True, exist_ok=True)
    for name in (".pipeline", "docs", "AGENTS.md"):
        src = TEMPLATE / name
        if not src.exists():
            continue
        dst = target / name
        if dst.exists():
            print(f"Preserved existing {name}; skipped.")
            continue
        if src.is_dir():
            shutil.copytree(src, dst, ignore=IGNORE)
        else:
            shutil.copy2(src, dst)
        print(f"Scaffolded: {name}")
    link = target / ".pipeline" / "scripts" / "link_skills.py"
    if link.exists():
        subprocess.check_call([sys.executable, str(link)], cwd=target)
    print(f"Scaffolded idea2product pipeline into {target}")
    return 0


# ---------------------------------------------------------------- adapters

def cmd_adapters(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    repo.mkdir(parents=True, exist_ok=True)
    agent = args.agent

    def want(name: str) -> bool:
        return agent in ("all", name)

    if want("cursor") and (ADAPTERS / "cursor" / ".cursor").exists():
        copy_tree(ADAPTERS / "cursor" / ".cursor", repo / ".cursor")

    if want("claude-code"):
        copy_file(ADAPTERS / "claude-code" / "CLAUDE.md", repo / "CLAUDE.md")
        n = copy_skill_dirs(SKILLS_SRC, repo / ".claude" / "skills")
        print(f"Installed {n} Claude Code project skills to {repo / '.claude' / 'skills'}")
        if args.install_user_skills:
            copy_skill_dirs(SKILLS_SRC, HOME / ".claude" / "skills")
            print(f"Installed user skills to {HOME / '.claude' / 'skills'}")

    if want("opencode") and (ADAPTERS / "opencode" / ".opencode").exists():
        copy_tree(ADAPTERS / "opencode" / ".opencode", repo / ".opencode")

    if want("hermes"):
        copy_file(ADAPTERS / "hermes" / "AGENTS.md", repo / "AGENTS.hermes.md")
        if args.install_user_skills:
            copy_skill_dirs(ADAPTERS / "hermes" / "skills", HOME / ".hermes" / "skills")
            print(f"Installed Hermes skills to {HOME / '.hermes' / 'skills'}")

    if want("openclaw"):
        copy_file(ADAPTERS / "openclaw" / "AGENTS.md", repo / "AGENTS.openclaw.md")
        copy_file(ADAPTERS / "openclaw" / "SOUL.md", repo / "SOUL.md")
        copy_file(ADAPTERS / "openclaw" / "TOOLS.md", repo / "TOOLS.md")
        copy_tree(ADAPTERS / "openclaw" / "skills", repo / "skills")
        if args.install_user_skills:
            copy_skill_dirs(ADAPTERS / "openclaw" / "skills", HOME / ".openclaw" / "skills")
            print(f"Installed OpenClaw skills to {HOME / '.openclaw' / 'skills'}")

    if want("generic"):
        copy_file(ADAPTERS / "generic" / "AGENTS.md", repo / "AGENTS.generic.md")

    if want("codex"):
        print("Codex uses 'install.py skills' and the scaffolded .agents/skills mapping.")

    copy_tree(ADAPTERS / "common", repo / "agent-adapters" / "common")
    print(f"Installed idea2product adapter(s) for '{agent}' into {repo}")
    return 0


# ---------------------------------------------------------------- main

def main() -> int:
    parser = argparse.ArgumentParser(prog="install.py", description="idea2product cross-platform installer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("skills", help="install entry skills for the user")
    s.add_argument("--target", choices=["both", "codex", "claude-code"], default="both")
    s.set_defaults(func=cmd_skills)

    sc = sub.add_parser("scaffold", help="create .pipeline + docs in a repository")
    sc.add_argument("repo")
    sc.set_defaults(func=cmd_scaffold)

    a = sub.add_parser("adapters", help="install host adapter files into a repository")
    a.add_argument("repo")
    a.add_argument("--agent", choices=["all", "codex", "cursor", "claude-code", "opencode", "hermes", "openclaw", "generic"], default="all")
    a.add_argument("--install-user-skills", action="store_true")
    a.set_defaults(func=cmd_adapters)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
