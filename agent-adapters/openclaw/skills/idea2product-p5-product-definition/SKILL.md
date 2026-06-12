---
name: idea2product-p5-product-definition
description: "Turn product discovery into delivery-ready product artifacts: PRD, user stories, acceptance criteria, edge cases, instrumentation, and PM critique before Product Gate. Use when the user explicitly asks for idea2product-P5-product-definition, P5, phase 5, or this step of the idea-to-product pipeline."
---

# idea2product-P5-product-definition

Turn product discovery into delivery-ready product artifacts: PRD, user stories, acceptance criteria, edge cases, instrumentation, and PM critique before Product Gate.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P5.

## Run

From the workspace root, run:

```powershell
python .pipeline/scripts/pipeline.py run P5
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/20-product/prd.md`

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python .pipeline/scripts/pipeline.py status` to confirm the workspace is consistent.
