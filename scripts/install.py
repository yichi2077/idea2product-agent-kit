#!/usr/bin/env python3
"""Cross-platform installer for the idea2product Agent Kit.

Works the same on Windows, macOS, and Linux. Python is the only requirement
(the same Python the pipeline already needs) -- no PowerShell, no bash.

Subcommands:
  init [repo]         One-shot onboarding: skills + scaffold + adapters (auto-detects host).
  skills              Install the 15 entry skills into the user's agent skill dir(s).
  scaffold <repo>     Create the .pipeline engine + docs inside a target repository.
  adapters <repo>     Install host adapter files into a target repository.
  upgrade <repo>      Update a scaffolded project's engine; preserves state, reports, and docs.
  speckit             Detect (or, with --install, install) Spec Kit -- the optional P7 dependency.

Examples:
  python3 scripts/install.py skills --target claude-code  # macOS/Linux
  python scripts/install.py skills --target claude-code   # Windows
  python3 scripts/install.py skills                       # both claude-code and codex
  python3 scripts/install.py scaffold /path/to/repo
  python3 scripts/install.py adapters /path/to/repo --agent all
  python3 scripts/install.py upgrade /path/to/repo
  python3 scripts/install.py speckit                      # show Spec Kit status + install commands
  python3 scripts/install.py speckit --install            # run the per-project Spec Kit init (needs uv)
  python3 scripts/install.py init /path/to/new-project    # one-shot onboarding (recommended)
"""
from __future__ import annotations

import argparse
import os
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

# Spec Kit is the OPTIONAL external dependency that pipeline phase P7 hands its
# Specify Packet off to (the speckit.* commands). The kit works without it; Spec Kit
# only adds the spec-driven implementation flow. See https://github.com/github/spec-kit
SPECKIT_REPO = "https://github.com/github/spec-kit"
SPECKIT_TOOL_INSTALL = "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
SPECKIT_GIT_REF = "git+https://github.com/github/spec-kit.git"


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


# ---------------------------------------------------------------- speckit

def speckit_init_cmd(project: str) -> list[str]:
    base = ["uvx", "--from", SPECKIT_GIT_REF, "specify", "init"]
    if project in (".", ""):
        # Existing repo / current directory: spec-kit uses --here for a non-empty dir.
        return base + ["--here", "--ai", "claude"]
    return base + [project, "--ai", "claude"]


def cmd_speckit(args: argparse.Namespace) -> int:
    project = args.project
    print("Spec Kit is the OPTIONAL external tool that pipeline phase P7 hands off to")
    print("(the speckit.* commands). The kit produces its Specify Packet without it.")
    print(f"Docs: {SPECKIT_REPO}\n")

    specify = shutil.which("specify")
    init_cmd = speckit_init_cmd(project)
    if specify:
        print(f"✓ Spec Kit CLI 'specify' is installed: {specify}")
        print("  Initialize this project with:")
        print("    " + " ".join(["specify", "init"] + init_cmd[init_cmd.index("init") + 1:]))
        return 0

    print("Spec Kit CLI 'specify' was not found on PATH. Recommended install commands:")
    print(f"  One-off (per project):  {' '.join(init_cmd)}")
    print(f"  Persistent CLI:         {SPECKIT_TOOL_INSTALL}")
    if not args.install:
        print("\nRe-run with --install to run the per-project init for you (requires 'uv').")
        return 0

    if not (shutil.which("uvx") or shutil.which("uv")):
        print("\nCannot auto-install: 'uv'/'uvx' is required but was not found.")
        print("  Install uv first: https://docs.astral.sh/uv/getting-started/installation/")
        return 1
    print(f"\nRunning: {' '.join(init_cmd)}")
    return subprocess.call(init_cmd)


# ---------------------------------------------------------------- upgrade

# Engine machinery is safe to replace from the canonical template on upgrade.
# Everything NOT listed here (state/, reports/, and the repo's docs/) is the user's
# work and is preserved untouched.
UPGRADE_MACHINERY = ["scripts", "recipes", "vendor", "custom-skills", "templates", "README.md"]


def cmd_upgrade(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    pipe = repo / ".pipeline"
    if not (pipe / "scripts" / "pipeline.py").exists():
        print(f"Not a scaffolded project (no .pipeline/scripts/pipeline.py): {repo}")
        print("Use 'scaffold' to create a new workspace instead.")
        return 2

    src_pipe = TEMPLATE / ".pipeline"
    updated: list[str] = []
    for name in UPGRADE_MACHINERY:
        src = src_pipe / name
        if not src.exists():
            continue
        dst = pipe / name
        backup_if_exists(dst)  # renames existing -> <name>.bak-<timestamp>, fully reversible
        if src.is_dir():
            shutil.copytree(src, dst, ignore=IGNORE)
        else:
            shutil.copy2(src, dst)
        updated.append(name)
        print(f"Upgraded .pipeline/{name}")

    print(f"\nUpgraded the engine in {repo}.")
    print("Preserved untouched: .pipeline/state/, .pipeline/reports/, docs/, AGENTS.md.")
    print("Replaced machinery was backed up in place as *.bak-<timestamp> (delete once verified).")
    print("Next: python3 .pipeline/scripts/pipeline.py doctor   # confirm the workspace is consistent")
    return 0


# ---------------------------------------------------------------- main

def detect_host() -> str:
    """Best-effort host detection from environment so `init` needs no flag."""
    env = os.environ
    if env.get("CODEX") or env.get("CODEX_SANDBOX"):
        return "codex"
    if env.get("CLAUDE_CODE") or env.get("CLAUDECODE") or env.get("ANTHROPIC_AGENT"):
        return "claude-code"
    if env.get("CURSOR_TRACE_ID") or env.get("CURSOR"):
        return "cursor"
    return "claude-code"


def cmd_init(args: argparse.Namespace) -> int:
    """One-shot onboarding: install skills, scaffold the engine, wire the host adapter.

    Designed to be run by the agent on the user's behalf so onboarding is a single
    command (no git/python steps for the user to type)."""
    repo = Path(args.repo).resolve()
    host = args.agent or detect_host()
    print(f"Initializing idea2product in {repo} (host: {host})\n")
    cmd_skills(argparse.Namespace(target="both"))
    cmd_scaffold(argparse.Namespace(repo=str(repo)))
    cmd_adapters(argparse.Namespace(repo=str(repo), agent=host, install_user_skills=False))
    print(f"\n✓ idea2product ready in {repo}.")
    print("In your agent, say:  run p1   (or invoke $idea2product-p0-guided-flow)")
    return 0


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

    up = sub.add_parser("upgrade", help="update a scaffolded project's engine (preserves state + docs)")
    up.add_argument("repo")
    up.set_defaults(func=cmd_upgrade)

    sk = sub.add_parser("speckit", help="detect or install Spec Kit (optional P7 dependency)")
    sk.add_argument("--project", default=".", help="project dir to init Spec Kit in (default: current dir)")
    sk.add_argument("--install", action="store_true", help="run the per-project Spec Kit init (requires uv)")
    sk.set_defaults(func=cmd_speckit)

    ini = sub.add_parser("init", help="one-shot onboarding: skills + scaffold + adapters (auto-detects host)")
    ini.add_argument("repo", nargs="?", default=".")
    ini.add_argument("--agent",
                     choices=["all", "codex", "cursor", "claude-code", "opencode", "hermes", "openclaw", "generic"],
                     default=None, help="host adapter to wire (default: auto-detect from environment)")
    ini.set_defaults(func=cmd_init)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
