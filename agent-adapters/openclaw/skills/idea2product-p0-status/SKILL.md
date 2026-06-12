---
name: idea2product-p0-status
description: "Report the current state of the idea-to-product pipeline, including active phase, mode, pilot validation state, gate states, and blockers, without changing pipeline files."
---

# idea2product-P0-status


    From the current workspace root, run:

    ```powershell
    python .pipeline/scripts/pipeline.py status
    ```

    If `.pipeline/scripts/pipeline.py` is missing, invoke `idea2product-p0-guided-flow` first to initialize the workspace, then report status. Summarize current phase, mode, pilot validation state, gate states, and any obvious blockers. Do not approve gates or edit state when only status was requested.
