# Pipeline User Guide

## Start

1. Put a real idea in `docs/00-idea/idea-brief.md`.
2. Run `python .pipeline/scripts/pipeline.py status`.
3. Run `python .pipeline/scripts/pipeline.py run P1`.
4. Follow the printed recipe and produce the listed outputs.

If the target project does not have `.pipeline/scripts/pipeline.py`, the `idea2product-p0-guided-flow` entry script initializes it automatically before running status, resume, or any P1-P9 phase command. Manual initialization is still available:

```powershell
python $env:USERPROFILE\.agents\skills\idea2product-p0-guided-flow\scripts\pipeline_entry.py init .
```

For existing projects, initialization is non-destructive by default: existing directories are merged, existing files are preserved, and an existing `AGENTS.md` is not overwritten.

## Daily Commands

- `python .pipeline/scripts/pipeline.py status`
- `python .pipeline/scripts/pipeline.py next`
- `python .pipeline/scripts/pipeline.py resume`
- `python .pipeline/scripts/pipeline.py run P1`
- `python .pipeline/scripts/pipeline.py gate request strategy`
- `python .pipeline/scripts/pipeline.py assumptions due`

## Codex Skills

Use `$idea2product-p0-guided-flow` for the guided end-to-end flow.

Use explicit phase skills when you already know the phase:

- `$idea2product-p1-idea-expansion`
- `$idea2product-p2-strategy-analysis`
- `$idea2product-p3-strategy-decision`
- `$idea2product-p4-product-discovery`
- `$idea2product-p5-product-definition`
- `$idea2product-p6-architecture-handoff`
- `$idea2product-p7-feature-specification`
- `$idea2product-p8-build-release`
- `$idea2product-p9-outcome-review`

Use `$idea2product-p0-status` to report current state and `$idea2product-p0-resume` to continue from the current state.

All entry skills are now self-bootstrapping through `$idea2product-p0-guided-flow`: if the project lacks `.pipeline`, the entry command initializes it before running the requested phase.

## Other Agents

This package includes adapters for Cursor, Claude Code, OpenCode, Hermes, OpenClaw, and generic `AGENTS.md`-compatible agents. Install them from the distribution package with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_agent_adapters.ps1 -TargetPath C:\path\to\repo -Agent all
```

See `docs/AGENT-ADAPTERS.md`.

## Gates

Agents can request a gate but cannot approve it. Approval requires a real terminal:

`python .pipeline/scripts/pipeline_gate.py approve strategy`

The command asks for the gate name and challenge. It refuses CI, pipes, redirects, and non-interactive shells.
