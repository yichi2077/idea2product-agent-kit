# idea2product Agent Operating Guide

idea2product is an Idea -> Strategy -> Product -> Architecture -> Delivery pipeline.

## Always Start Here

From the repository root:

```bash
python3 .pipeline/scripts/pipeline.py status
python3 .pipeline/scripts/pipeline.py resume
```

On Windows:

```powershell
python .pipeline/scripts/pipeline.py status
python .pipeline/scripts/pipeline.py resume
```

If `.pipeline/scripts/pipeline.py` does not exist, the pipeline is not installed in this workspace. Scaffold it before running phase work.

## Phase Map

- P0 guided flow: decide whether to report status, resume, ask for a real idea, run diagnostics, retire, or run the next phase.
- P0 status: report current phase, pilot validation state, gates, and blockers.
- P0 resume: report state and recommend the next command.
- P0 rollback: reopen a completed phase after explicit target, affected reports, reason, and confirmation.
- P0 doctor: run the read-only health check for state, recipes, gates, completed outputs, and stale artifacts.
- P0 retire: retire or archive the project after explicit confirmation and a non-empty reason.
- P1 idea expansion: capture a real idea and initialize assumptions and risks.
- P2 existing solutions scan: search for ready-to-use products, services, open-source projects, and substitute workflows; require a user decision before deeper strategy work.
- P2 strategy analysis: issue tree, hypothesis tree, market, competition, unit economics, options, evidence, unknowns.
- P3 strategy decision: decision memo, recommendation, red-team, Strategy Gate request.
- P4 product discovery: product thesis, target user, problem, JTBD, value proposition, boundaries.
- P5 product definition: PRD, stories, acceptance criteria, edge cases, instrumentation, PM critique.
- P6 architecture handoff: feature map, traceability, options, spikes, ADRs.
- P7 feature specification: one MVP feature at a time using approved PRD and ADRs.
- P8 build release: implementation, verification, launch/GTM checklist, Release Gate request.
- P9 outcome review: update assumptions, risks, decision log, PRD, or ADRs based on real outcomes.

## Commands

```bash
python3 .pipeline/scripts/pipeline.py status
python3 .pipeline/scripts/pipeline.py resume
python3 .pipeline/scripts/pipeline.py handoff
python3 .pipeline/scripts/pipeline.py doctor
python3 .pipeline/scripts/pipeline.py run P1
python3 .pipeline/scripts/pipeline.py run P2
python3 .pipeline/scripts/pipeline.py run P3
python3 .pipeline/scripts/pipeline.py run P4
python3 .pipeline/scripts/pipeline.py run P5
python3 .pipeline/scripts/pipeline.py run P6
python3 .pipeline/scripts/pipeline.py run P7
python3 .pipeline/scripts/pipeline.py run P8
python3 .pipeline/scripts/pipeline.py run P9
python3 .pipeline/scripts/pipeline.py gate request strategy
python3 .pipeline/scripts/pipeline.py reopen P5 --reason "reason from the user"
python3 .pipeline/scripts/pipeline.py retire --reason "reason from the user"
python3 .pipeline/scripts/pipeline.py assumptions due
```

## Gate Rules

Gates are human-owned: agents may REQUEST a gate and can never *skip* one, but the human
decides. The mode (`pipeline.py gate mode [light|strict]`) governs how the verdict is recorded:

- **light (default):** after the user explicitly approves or rejects in the conversation,
  the agent records it with the user's reason (no separate terminal):
  ```bash
  python3 .pipeline/scripts/pipeline_gate.py approve strategy --rationale "<the user's reason>"
  python3 .pipeline/scripts/pipeline_gate.py reject strategy --rationale "<the user's reason>"
  ```
- **strict (opt-in):** the agent cannot approve. The human runs it in a plain OS terminal
  (not the agent's integrated terminal) and types the gate name, the challenge printed at
  request time, and a note (`python` on Windows):
  ```bash
  python3 .pipeline/scripts/pipeline_gate.py approve strategy
  ```

The agent must never approve without the user's explicit decision in the conversation.

A rejected gate can be re-opened by requesting it again. Do not bypass with direct
state edits, `--yes`, `--force`, CI, pipes, redirects, or environment variables.

## Real Idea Rule

Do not invent a fake business idea for P1-P3 validation. If `docs/00-idea/idea-brief.md` is missing or scaffold-only, ask the user for a real idea.

## Verification

After changing pipeline state or artifacts, confirm the workspace is still in a coherent state:

```bash
python3 .pipeline/scripts/pipeline.py status
python3 .pipeline/scripts/pipeline.py handoff
```

On Windows:

```powershell
python .pipeline/scripts/pipeline.py status
python .pipeline/scripts/pipeline.py handoff
```

Use the dedicated skills for user-facing operations when available:
`$idea2product-p0-status`, `$idea2product-p0-resume`, `$idea2product-p0-rollback`,
`$idea2product-p0-doctor`, and `$idea2product-p0-retire`. Use
`$idea2product-p2-strategy-analysis` for P2; it includes the existing-solutions
scan as a required first step.
