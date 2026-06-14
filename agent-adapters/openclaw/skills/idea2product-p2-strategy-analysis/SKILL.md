---
name: idea2product-p2-strategy-analysis
description: "Analyze the approved idea as a strategy problem, starting with an existing-solutions scan so the user can use, buy, partner, retire, or deliberately build a differentiated product before deeper strategy work. Use when the user explicitly asks for idea2product-P2-strategy-analysis, P2, phase 2, or this step of the idea-to-product pipeline."
---

# idea2product-P2-strategy-analysis

Analyze the approved idea as a strategy problem. Start by checking whether an
existing product, service, open-source project, or substitute workflow already solves
the idea well enough that the user should use, buy, partner, or retire instead of
building. Only then continue into issue tree, hypothesis tree, market, competition,
trend, right to win, unit economics, strategic options, evidence quality, and unknowns.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P2.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P2
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P2
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/10-strategy/existing-solutions-scan.md`

`docs/10-strategy/strategy-research-note.md`

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- Run `$idea2product-p2-existing-solutions-scan` first. If the scan finds a ready
  existing solution, stop and get the user's decision before continuing.
- Do not complete P2 while `existing-solutions-scan.md` has `User Decision: pending`
  or says the user chose `use_existing` / `retire`.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
