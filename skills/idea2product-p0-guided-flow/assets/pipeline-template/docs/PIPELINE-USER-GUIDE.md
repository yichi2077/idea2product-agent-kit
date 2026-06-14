# Pipeline User Guide

The primary interface is skills: tell your agent *"Use idea2product-p0-guided-flow"* (or `$idea2product-p0-guided-flow` in Codex) and it operates the pipeline for you. The `pipeline.py` commands in this guide are what the **agent** runs on your behalf — the deterministic engine behind the skills. You can run the read-only ones (`status`, `handoff`) yourself to look under the hood, but the only command you run directly in normal use is **gate approval**, in a real terminal. Direct `pipeline_entry.py` initialization is a low-level tooling path; the recommended user path is guided-flow first, so onboarding captures the idea before scaffolding.

## Start

What the agent does when you invoke the guided flow:

1. Explains the kit and asks for your idea before initializing a new workspace.
2. Captures your real idea in `docs/00-idea/idea-brief.md` (P1).
3. Runs `pipeline.py handoff` to orient, and summarizes it for you.
4. Runs the next phase via the matching `idea2product-Px-*` skill.
5. Follows the printed recipe, produces the listed outputs, and completes the phase only after those outputs are real rather than scaffold placeholders. In P2, the first required output is an existing-solutions scan so the agent can warn you when a ready-to-use product may already solve the idea.

If the target project does not have `.pipeline/scripts/pipeline.py`, the `idea2product-p0-guided-flow` entry script auto-initializes only an empty directory or a `.git`-only empty repo. In a non-empty project, initialize explicitly after confirming the target:

```powershell
python $env:USERPROFILE\.agents\skills\idea2product-p0-guided-flow\scripts\pipeline_entry.py init .
```

For existing projects, initialization is non-destructive by default: existing directories are merged, existing files are preserved, and an existing `AGENTS.md` is not overwritten.

## Commands the agent runs

These back the skills; the agent runs them for you (use `python3` on macOS/Linux, `python` on Windows). The read-only ones you can run yourself to look under the hood; the last one is the only command **you** run directly.

| Command | Purpose |
| --- | --- |
| `pipeline.py handoff` | read-only brief: phase, next step, gates, decisions, open assumptions/risks, stale outputs |
| `pipeline.py status` / `next` / `resume` | current state (+ stale warnings) / next correct step / re-orient and continue |
| `pipeline.py doctor` | read-only workspace health check: template files, recipes, registers, state invariants, stale outputs |
| `pipeline.py run P1` … `run P9` | print and execute a phase recipe |
| `pipeline.py stage complete <phase>` | mark only the current ready phase complete after required outputs exist and are no longer scaffold placeholders |
| `pipeline.py gate request <gate> --confidence high\|medium\|low --rationale "…"` | request a gate with stated confidence (agent only) |
| `pipeline.py reopen P5 --reason "…"` | rework a completed upstream phase and reset downstream |
| `pipeline.py retire --reason "…"` | abandon a project pre-release after explicit confirmation |
| `pipeline.py assumptions due` | assumptions and risks past their review date |
| `pipeline_gate.py approve <gate>` | **you**, in a real OS terminal — approve a requested gate |

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

Use `$idea2product-p0-status` to report current state, `$idea2product-p0-resume` to continue from the current state, `$idea2product-p0-doctor` to health-check state and artifacts, and `$idea2product-p0-retire` to retire the project after confirmation.

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

### Confidence signal

When an agent requests a gate it should state how confident it is in the decision context it prepared:

`pipeline.py gate request strategy --confidence high|medium|low --rationale "what drives that confidence"`

The level and rationale are recorded in `.pipeline/state/phase-metadata.json` and shown to you at approval time, so you can vary your scrutiny accordingly. A `low` or unstated confidence prints a caution before the challenge prompt. Confidence is advisory only — it never auto-approves or auto-rejects, because a self-rated score is not a reliable gate. Ground the rationale in the open assumptions and risks (`pipeline.py handoff`).

## Handoff Brief

When you return after a break, or a fresh agent session (or a different model) picks up the work, run `pipeline.py handoff` before doing anything else. It is a read-only renderer that consolidates the five things needed to continue without re-litigating settled work: current phase, the next step, gate states, the decisions already recorded, the open assumptions and risks (flagged `OVERDUE` past their review date), and any stale completed outputs. It reads only the registers the pipeline already maintains and never changes state. `resume` points to it.

## Rework Loops

Use `pipeline.py reopen Px --reason "..."` when downstream work proves an upstream phase is stale or wrong. Reopen moves the target phase back to `ready`, resets downstream phases to `waiting`, clears affected gates, records the reason in `.pipeline/state/decision-log.md`, and drops stale phase hashes from `.pipeline/state/phase-metadata.json`.

`status` and `next` warn when a completed phase output changes after completion. Treat those warnings as a prompt to either confirm the change is harmless or reopen the affected phase before requesting the next gate.

Product Gate requires a real PRD and a real PM critic report. Strategy Gate requires a real decision memo and `.pipeline/reports/strategy-red-team.md`.

## Existing Solutions Scan

P2 starts by checking whether the expanded idea already has a ready-to-use solution.
The agent uses the required first step inside `$idea2product-p2-strategy-analysis`
to search for direct competitors, indirect competitors, substitute workflows,
open-source projects, SaaS, apps, services, templates, and no-code tools. The
result is written to `docs/10-strategy/existing-solutions-scan.md`.

If the scan finds a perfect or good-enough solution, the agent must pause and ask
whether you want to use/buy/partner, build a differentiated wedge, continue research,
or retire. P2 cannot complete while the scan's `User Decision` is `pending`, `use_existing`,
or `retire`.

## Health Check and Retire

Use `$idea2product-p0-doctor` when the workspace may be inconsistent. It runs
`pipeline.py doctor` read-only and reports missing files, scaffold outputs, stale
completed outputs, and gate/state invariant issues.

Use `$idea2product-p0-retire` only when abandoning or archiving the project. It must
show the current handoff, collect explicit confirmation and a non-empty reason, then
run `pipeline.py retire --reason "..."`. It does not delete files; future work requires
reopening a completed phase.
