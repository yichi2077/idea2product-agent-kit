---
name: idea2product-p4-product-discovery
description: "Translate an approved strategy into product discovery: target user, problem statement, jobs-to-be-done, value proposition, business model, boundaries, product hypotheses, and stop conditions. Use when the user explicitly asks for idea2product-P4-product-discovery, P4, phase 4, or this step of the idea-to-product pipeline."
---

# idea2product-P4-product-discovery

Translate an approved strategy into product discovery: target user, problem statement, jobs-to-be-done, value proposition, business model, boundaries, product hypotheses, and stop conditions.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P4.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P4
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P4
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/20-product/product-thesis.md`

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
