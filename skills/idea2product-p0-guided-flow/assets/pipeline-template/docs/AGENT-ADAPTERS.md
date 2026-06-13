# Agent Adapters

idea2product is no longer Codex-only. The core pipeline remains `.pipeline`, while adapters teach each host how to operate the same state machine.

## Shared Contract

Every host should:

1. Start with `python3 .pipeline/scripts/pipeline.py status` on macOS/Linux, or `python .pipeline/scripts/pipeline.py status` on Windows.
2. Use `python3 .pipeline/scripts/pipeline.py resume` on macOS/Linux, or `python .pipeline/scripts/pipeline.py resume` on Windows, to determine the next action.
3. Run exactly one phase command at a time: `run P1` through `run P9`.
4. Never approve gates from the agent runtime.
5. Ask the user for a real idea when P1-P3 validation lacks `docs/00-idea/idea-brief.md`.
6. Run `pipeline.py status` and `pipeline.py handoff` after changing pipeline state or artifacts.

If `.pipeline/scripts/pipeline.py` is missing, the installed idea2product guided skill auto-initializes only empty directories or `.git`-only empty repos. For non-empty projects, initialize explicitly after confirming the target:

```powershell
python $env:USERPROFILE\.agents\skills\idea2product-p0-guided-flow\scripts\pipeline_entry.py init .
```

Package-based installs may alternatively run `scripts/scaffold_into_repo.ps1`. Initialization is non-destructive by default; use `--force` only when the user explicitly wants to overwrite existing scaffold files.

## Adapter Matrix

| Host | Adapter | Notes |
| --- | --- | --- |
| Codex | `$HOME/.agents/skills` plus repo `.agents/skills` | Uses `idea2product-p0-guided-flow`, P1-P9 skills, status, and resume. |
| Cursor | `.cursor/rules/idea2product.mdc` | Project rule points Cursor at the shared guide. |
| Claude Code | `CLAUDE.md` | Project memory points Claude Code at the shared guide and pipeline commands. |
| OpenCode | `AGENTS.md` and `.opencode/agents/idea2product.md` | OpenCode supports project instructions and markdown-defined agents. |
| Hermes | `AGENTS.md` and `~/.hermes/skills` | Hermes can use context files plus AgentSkills-compatible skills. |
| OpenClaw | `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `skills/` | OpenClaw can load workspace skills and bootstrap files. |
| Generic | `AGENTS.md` | For agents that only support project instruction markdown. |

## Install From Package

After scaffolding the pipeline into a target repository:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_agent_adapters.ps1 -TargetPath C:\path\to\repo -Agent all
```

Use `-Agent cursor`, `-Agent claude-code`, `-Agent opencode`, `-Agent hermes`, `-Agent openclaw`, or `-Agent generic` for one host.

Use `-InstallUserSkills` with Hermes or OpenClaw to copy AgentSkills-compatible skills into their user skill directories.
