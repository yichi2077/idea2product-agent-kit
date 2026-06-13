---
name: idea2product-p3-strategy-decision
description: "Convert strategy analysis into a decision memo comparing build, buy, partner, capability-only, internal improvement, wait, and do-nothing options, then red-team the recommendation and request Strategy Gate. Use when the user explicitly asks for idea2product-P3-strategy-decision, P3, phase 3, or this step of the idea-to-product pipeline."
---

# idea2product-P3-strategy-decision

Convert strategy analysis into a decision memo comparing build, buy, partner, capability-only, internal improvement, wait, and do-nothing options, then red-team the recommendation and request Strategy Gate.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P3.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P3
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P3
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/10-strategy/decision-memo.md`

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
