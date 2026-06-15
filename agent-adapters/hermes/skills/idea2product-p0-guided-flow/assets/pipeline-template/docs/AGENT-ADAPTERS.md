# Agent Adapters

idea2product is no longer Codex-only. The core pipeline remains `.pipeline`, while adapters teach each host how to operate the same state machine.

## Shared Contract

Every host should:

1. Start with `python3 .pipeline/scripts/pipeline.py status` on macOS/Linux, or `python .pipeline/scripts/pipeline.py status` on Windows.
2. Use `python3 .pipeline/scripts/pipeline.py resume` on macOS/Linux, or `python .pipeline/scripts/pipeline.py resume` on Windows, to determine the next action.
3. Run exactly one phase command at a time: `run P1` through `run P9`.
4. Never approve gates autonomously. In **light** mode (default) you may RECORD the user's explicit in-chat approval via `pipeline_gate.py approve <gate> --rationale "…"`; in **strict** mode you cannot approve at all (the user approves in a real terminal). Either way, never approve without the user's explicit decision in the conversation.
5. Ask the user for a real idea when P1-P3 validation lacks `docs/00-idea/idea-brief.md`.
6. Use `pipeline.py doctor` for read-only health checks when state or artifacts look inconsistent.
7. Use `pipeline.py retire --reason "..."` only after explicit confirmation and a user-provided reason.
8. Run `pipeline.py status` and `pipeline.py handoff` after changing pipeline state or artifacts.

If `.pipeline/scripts/pipeline.py` is missing, scaffold it first — the recommended cross-platform path is the one-shot initializer (the agent runs it for the user):

```bash
python3 scripts/install.py init /path/to/repo   # use `python` on Windows
```

Scaffolding is non-destructive: existing `.pipeline`, `docs/`, and state are preserved.

## Adapter Matrix

| Host | Adapter | Notes |
| --- | --- | --- |
| Codex | `$HOME/.agents/skills` plus repo `.agents/skills` | Uses `idea2product-p0-guided-flow`, P1-P10 skills, status, resume, rollback, doctor, and retire. |
| Cursor | `.cursor/rules/idea2product.mdc` | Project rule points Cursor at the shared guide. |
| Claude Code | `CLAUDE.md` | Project memory points Claude Code at the shared guide and pipeline commands. |
| OpenCode | `AGENTS.md` and `.opencode/agents/idea2product.md` | OpenCode supports project instructions and markdown-defined agents. |
| Hermes | `AGENTS.md` and `~/.hermes/skills` | Hermes can use context files plus AgentSkills-compatible skills. |
| OpenClaw | `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `skills/` | OpenClaw can load workspace skills and bootstrap files. |
| Generic | `AGENTS.md` | For agents that only support project instruction markdown. |

## Install Adapters

Cross-platform (recommended):

```bash
python3 scripts/install.py adapters /path/to/repo --agent all   # use `python` on Windows
```

Use `-Agent cursor`, `-Agent claude-code`, `-Agent opencode`, `-Agent hermes`, `-Agent openclaw`, or `-Agent generic` for one host.

Use `-InstallUserSkills` with Hermes or OpenClaw to copy AgentSkills-compatible skills into their user skill directories.
