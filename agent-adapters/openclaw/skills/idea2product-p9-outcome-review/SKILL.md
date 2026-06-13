---
name: idea2product-p9-outcome-review
description: "Review real outcomes after release, decide continue, scale, iterate, pivot, pause, or retire, and update assumptions, risks, decision log, PRD, or ADRs rather than only writing a retrospective. Use when the user explicitly asks for idea2product-P9-outcome-review, P9, phase 9, or this step of the idea-to-product pipeline."
---

# idea2product-P9-outcome-review

Review real outcomes after release, decide continue, scale, iterate, pivot, pause, or retire, and update assumptions, risks, decision log, PRD, or ADRs rather than only writing a retrospective.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P9.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P9
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P9
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/40-delivery/outcome-review.md`

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
