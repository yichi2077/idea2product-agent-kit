# Phase2 Dogfood Pilot: Feedback Loop Hardening

Date: 2026-06-12
Branch: `codex/phase2-feedback-loop-hardening`
Pilot idea: `idea2product Phase2 Feedback Loop Hardening`

## Summary

This pilot used idea2product itself as the real idea for P1-P3. The goal was to validate the Phase2 increment: add explicit rework loops, artifact staleness detection, gate evidence preconditions, and state invariant checks before adding lower-priority analytics connectors or deck generation.

## Execution Evidence

- Scaffolded a temporary workspace with `python3 scripts/install.py scaffold <tmpdir>`.
- Replaced scaffold placeholders with real P1-P3 artifacts.
- Ran:
  - `python3 .pipeline/scripts/pipeline.py stage complete P1`
  - `python3 .pipeline/scripts/pipeline.py stage complete P2`
  - `python3 .pipeline/scripts/pipeline.py stage complete P3`
  - `python3 .pipeline/scripts/pipeline.py gate request strategy`
- Final state: `P1`, `P2`, and `P3` complete; `P4` blocked until Strategy Gate; Strategy Gate awaiting human approval.

## Gate Request Output

```text
Gate requested: strategy
Manual approval challenge: 5D43D0
Approval must be performed by a human in a real interactive terminal using pipeline_gate.py.
```

## Friction Log

| Step | Observation | Follow-up |
|---|---|---|
| Template verify | Running `verify.sh` directly inside `pipeline-template/` needed `.agents/skills`; fixed by making verify run `link_skills.py` first. | Covered by verify. |
| State loop | Sidecar JSON was simpler and safer than embedding hash metadata in the YAML state. | Keep runtime stdlib-only. |
| Pilot status | P3 completion originally left `pilot_validation` as `PENDING_REAL_IDEA`; fixed to mark `P1_P3_AWAITING_STRATEGY_APPROVAL`. | Strategy approval path marks `P1_P3_STRATEGY_GATE_APPROVED`. |
| Evidence wiring | Strategy Gate now requires decision memo plus red-team report in standard/high-assurance mode. | Dogfood gate request proves the preconditions pass with real artifacts. |

## A-0001 Disposition

The original assumption, "First real idea is not supplied yet; pilot P1-P3 remains pending," is no longer true for this branch's dogfood evidence. The real idea is captured in `idea-brief.md`, and the state snapshot records `pilot_validation: "P1_P3_AWAITING_STRATEGY_APPROVAL"`.
