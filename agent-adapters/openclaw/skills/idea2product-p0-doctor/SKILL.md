---
name: idea2product-p0-doctor
description: "Run the idea-to-product pipeline health check from the current workspace, report whether pipeline state and required artifacts are coherent, and never change pipeline state."
---

# idea2product-P0-doctor

Use this when the user asks whether the workspace is healthy, consistent, OK to
continue, or when pipeline state/files appear to disagree. This is a read-only
diagnostic skill: you run the health check for the user and summarize the result.

## Precheck

1. Walk upward from the current directory until `.pipeline/scripts/pipeline.py` exists.
2. If it does not exist, this workspace has no pipeline yet — tell the user to run
   `$idea2product-p0-guided-flow` to initialize it, then stop. Do not scaffold from
   this skill.

## Execute

From the workspace root, run the doctor command (use `python` on Windows):

```bash
python3 .pipeline/scripts/pipeline.py doctor
```

Doctor checks the pipeline template, recipes, state registers, gate invariants,
completed phase outputs, and stale artifacts that matter for the current state.
It is intentionally stricter for completed phases than for fresh scaffold state.

## Report

Summarize the result in plain language:

- If healthy, say the pipeline is healthy and name the next useful action
  (`$idea2product-p0-resume`, `$idea2product-p0-status`, or the ready phase skill).
- If unhealthy, list the concrete failures from the command: missing files, scaffold
  outputs that still need replacement, stale completed outputs, gate invariant
  failures, or other state inconsistencies.
- If the command exits non-zero, do not continue phase work until the user resolves
  or explicitly asks to repair the listed issue.

## Never

- Never edit state files or artifacts from this skill.
- Never approve gates, complete phases, reopen phases, or retire projects.
- Never treat a healthy fresh scaffold as proof that phase outputs are ready; phase
  completion still belongs to the relevant phase skill and engine validation.
