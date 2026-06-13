---
name: idea2product-p0-status
description: "Report the current state of the idea-to-product pipeline, including active phase, mode, pilot validation state, gate states, and blockers, without changing pipeline files."
---

# idea2product-P0-status

From the current workspace root, run (use `python` on Windows):

```bash
python3 .pipeline/scripts/pipeline.py status
```

`status` prints the state and any stale-artifact warnings. For the full consolidated brief (decisions, open assumptions/risks, next step) run `pipeline.py handoff` instead. You run these for the user; they do not type them.

If `.pipeline/scripts/pipeline.py` is missing, invoke `idea2product-p0-guided-flow` first to initialize the workspace, then report status. Summarize current phase, mode, pilot validation state, gate states, stale warnings, and any obvious blockers. Do not approve gates or edit state when only status was requested.
