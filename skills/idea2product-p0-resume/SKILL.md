---
name: idea2product-p0-resume
description: "Resume the idea-to-product pipeline from saved state by reporting current status, identifying the next ready phase or blocker, and continuing only when the user asked to proceed."
---

# idea2product-P0-resume

From the current workspace root, run the read-only handoff brief (it is the right way to re-orient after a break or in a fresh session) — use `python` on Windows:

```bash
python3 .pipeline/scripts/pipeline.py handoff
```

It consolidates current phase, the next step, gate states, the decisions already recorded, open assumptions and risks, and any stale outputs. Summarize it for the user; you operate the pipeline, the user does not type these commands.

If `.pipeline/scripts/pipeline.py` is missing, invoke `idea2product-p0-guided-flow` first to initialize the workspace, then resume. If a completed output is reported **stale**, raise it before continuing. If the next phase is ready and the user asked to continue rather than only report, use the corresponding `idea2product-Px-*` skill. If a gate or a real idea is missing, stop and state the missing user action (gate approval is the user's to run, not yours).
