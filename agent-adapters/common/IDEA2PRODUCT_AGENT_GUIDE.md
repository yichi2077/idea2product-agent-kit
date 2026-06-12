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

- P0 guided flow: decide whether to report status, resume, ask for a real idea, or run the next phase.
- P0 status: report mode, current phase, pilot validation state, gates, and blockers.
- P0 resume: report state and recommend the next command.
- P1 idea expansion: capture a real idea and initialize assumptions and risks.
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
python3 .pipeline/scripts/pipeline.py assumptions due
```

## Gate Rules

Agents may request gates but must not approve gates.

Human approval or rejection requires a real interactive terminal (a plain OS
terminal, not an agent's integrated terminal). The human types the gate name, the
random challenge printed at request time, and a non-empty note:

```powershell
python .pipeline/scripts/pipeline_gate.py approve strategy
python .pipeline/scripts/pipeline_gate.py reject strategy
```

On macOS/Linux, use `python3` for the same gate commands.

A rejected gate can be re-opened by requesting it again. Do not bypass with direct
state edits, `--yes`, `--force`, CI, pipes, redirects, or environment variables.

## Real Idea Rule

Do not invent a fake business idea for P1-P3 validation. If `docs/00-idea/idea-brief.md` is missing or scaffold-only, ask the user for a real idea.

## Verification

After changing pipeline files:

```bash
sh .pipeline/scripts/verify.sh
```

On Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .pipeline/scripts/verify.ps1
```
