---
name: idea2product-p6-validation-prototype
description: "Validate the single core interaction with a throwaway prototype tested on ~5 target users before committing to architecture and full build; the conversations are the evidence, not the prototype. Use when the user explicitly asks for idea2product-P6-validation-prototype, P6, phase 6, or this step of the idea-to-product pipeline."
---

# idea2product-P6-validation-prototype

Validate the single core, indispensable interaction with the smallest throwaway prototype, put it in front of ~5 target-persona users, and observe behavior (not stated preference) before investing in architecture and full build. The prototype is a prop; the conversations are the evidence. This phase is waivable with a recorded rationale (no hard floor).

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P6.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P6
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P6
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/20-product/validation-prototype.md`

## Rules

- Do not skip earlier gates or approved dependencies.
- The prototype's existence is not evidence — record the user conversations and the observed behavior, and whether you sought disconfirming signal.
- This phase is waivable: if you deliberately skip the prototype, set `Decision: skip_with_rationale` in the output and record the accepted risk in the registers. Never silently skip.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
