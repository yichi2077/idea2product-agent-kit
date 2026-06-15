---
name: idea2product-p8-feature-specification
description: "Specify one MVP feature at a time from approved PRD and ADR context, producing Spec Kit-ready packets and implementation planning without reopening product-level decisions. Use when the user explicitly asks for idea2product-P8-feature-specification, P8, phase 8, or this step of the idea-to-product pipeline."
---

# idea2product-P8-feature-specification

Specify one MVP feature at a time from approved PRD and ADR context, producing Spec Kit-ready packets and implementation planning without reopening product-level decisions.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P8.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P8
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P8
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/30-architecture/specify-packets/`

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- If the command reports a blocker, report the blocker and the concrete missing input.
- If the engine reports Spec Kit is not detected, install it yourself by running the exact command the engine printed (the `uvx --from git+… specify init …` line), then continue and report that you configured Spec Kit. Never tell the user to open a terminal to install it.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
