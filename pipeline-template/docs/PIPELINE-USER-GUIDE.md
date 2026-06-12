# Pipeline User Guide

## Start

1. Put a real idea in `docs/00-idea/idea-brief.md`.
2. Run `python3 .pipeline/scripts/pipeline.py status` on macOS/Linux, or `python .pipeline/scripts/pipeline.py status` on Windows.
3. Run `python3 .pipeline/scripts/pipeline.py run P1` on macOS/Linux, or `python .pipeline/scripts/pipeline.py run P1` on Windows.
4. Follow the printed recipe and produce the listed outputs.

If the target project does not have `.pipeline/scripts/pipeline.py`, the `idea2product-p0-guided-flow` entry script auto-initializes only an empty directory or a `.git`-only empty repo. In a non-empty project, initialize explicitly after confirming the target:

```powershell
python $env:USERPROFILE\.agents\skills\idea2product-p0-guided-flow\scripts\pipeline_entry.py init .
```

For existing projects, initialization is non-destructive by default: existing directories are merged, existing files are preserved, and an existing `AGENTS.md` is not overwritten.

## Daily Commands

- `python3 .pipeline/scripts/pipeline.py status` on macOS/Linux; `python .pipeline/scripts/pipeline.py status` on Windows
- `python3 .pipeline/scripts/pipeline.py next` on macOS/Linux; `python .pipeline/scripts/pipeline.py next` on Windows
- `python3 .pipeline/scripts/pipeline.py resume` on macOS/Linux; `python .pipeline/scripts/pipeline.py resume` on Windows
- `python3 .pipeline/scripts/pipeline.py handoff` on macOS/Linux; `python .pipeline/scripts/pipeline.py handoff` on Windows
- `python3 .pipeline/scripts/pipeline.py run P1` on macOS/Linux; `python .pipeline/scripts/pipeline.py run P1` on Windows
- `python3 .pipeline/scripts/pipeline.py gate request strategy` on macOS/Linux; `python .pipeline/scripts/pipeline.py gate request strategy` on Windows
- `python3 .pipeline/scripts/pipeline.py reopen P5 --reason "..."` on macOS/Linux; `python .pipeline/scripts/pipeline.py reopen P5 --reason "..."` on Windows
- `python3 .pipeline/scripts/pipeline.py assumptions due` on macOS/Linux; `python .pipeline/scripts/pipeline.py assumptions due` on Windows

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

All entry skills are self-bootstrapping through `$idea2product-p0-guided-flow`: if the project lacks `.pipeline`, the entry command initializes empty targets automatically and requires explicit `init .` or `--auto-init` for non-empty targets.

## Other Agents

This package includes adapters for Cursor, Claude Code, OpenCode, Hermes, OpenClaw, and generic `AGENTS.md`-compatible agents. Install them from the distribution package with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_agent_adapters.ps1 -TargetPath C:\path\to\repo -Agent all
```

See `docs/AGENT-ADAPTERS.md`.

## Gates

Agents can request a gate but cannot approve it. Approval requires a real terminal:

`python3 .pipeline/scripts/pipeline_gate.py approve strategy` on macOS/Linux, or `python .pipeline/scripts/pipeline_gate.py approve strategy` on Windows.

The command asks for the gate name and challenge. It refuses CI, pipes, redirects, and non-interactive shells.

## Handoff Brief

When you return after a break, or a fresh agent session (or a different model) picks up the work, run `pipeline.py handoff` before doing anything else. It is a read-only renderer that consolidates the five things needed to continue without re-litigating settled work: current phase and mode, the next step, gate states, the decisions already recorded, the open assumptions (flagged `OVERDUE` past their review date) and open risks, and any stale completed outputs. It reads only the registers the pipeline already maintains and never changes state. `resume` points to it.

## Rework Loops

Use `pipeline.py reopen Px --reason "..."` when downstream work proves an upstream phase is stale or wrong. Reopen moves the target phase back to `ready`, resets downstream phases to `waiting`, clears affected gates, records the reason in `.pipeline/state/decision-log.md`, and drops stale phase hashes from `.pipeline/state/phase-metadata.json`.

`status` and `next` warn when a completed phase output changes after completion. Treat those warnings as a prompt to either confirm the change is harmless or reopen the affected phase before requesting the next gate.

Product Gate requires a real PRD and a real PM critic report. Strategy Gate in standard/high-assurance mode requires a real decision memo and `.pipeline/reports/strategy-red-team.md`.
