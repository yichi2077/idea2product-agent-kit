---
name: idea2product-p7-architecture-handoff
description: "Bridge product definition into technical direction by creating feature maps, traceability, architecture options, spikes, design rationale, and ADRs before Architecture Gate. Use when the user explicitly asks for idea2product-P7-architecture-handoff, P7, phase 7, or this step of the idea-to-product pipeline."
---

# idea2product-P7-architecture-handoff

Bridge product definition into technical direction by creating feature maps, traceability, architecture options, spikes, design rationale, and ADRs before Architecture Gate.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P7.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P7
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P7
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/30-architecture/feature-map.yaml`

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
