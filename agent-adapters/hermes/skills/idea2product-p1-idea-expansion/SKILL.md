---
name: idea2product-p1-idea-expansion
description: "Capture a real product or business idea as a falsifiable hypothesis, clarify the user, frequency, quantified loss, workaround, urgency, do-nothing cost, risks, and stop conditions, then initialize assumptions and risks for downstream strategy work. Use when the user explicitly asks for idea2product-P1-idea-expansion, P1, phase 1, or this step of the idea-to-product pipeline."
---

# idea2product-P1-idea-expansion

Capture a real product or business idea as a falsifiable hypothesis, clarify the
specific user, scenario, frequency, quantified loss, current workaround, urgency,
do-nothing cost, time budget, risks, and stop conditions, then initialize
assumptions and risks for downstream strategy work.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P1.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P1
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P1
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/00-idea/idea-brief.md`

## Founder's Playbook Focus

The key deliverable is not a polished pitch. It is a testable sentence:
`[persona] in [scenario] every [frequency] hits [problem] because [cause], costing them [quantified loss]`.
If the persona, frequency, loss, or workaround is vague, ask the user to sharpen
it before completing P1.

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
