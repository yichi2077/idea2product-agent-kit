---
name: idea2product-p0-resume
description: "Resume the idea-to-product pipeline from saved state by reporting current status, identifying the next ready phase or blocker, and continuing only when the user asked to proceed."
---

# idea2product-P0-resume


    From the current workspace root, run:

    ```powershell
    python .pipeline/scripts/pipeline.py resume
    ```

    If `.pipeline/scripts/pipeline.py` is missing, invoke `idea2product-p0-guided-flow` first to initialize the workspace, then resume. Explain the recommended next command. If the next phase is ready and the user asked to continue rather than only report, use the corresponding `idea2product-Px-*` skill. If a gate or real idea is missing, stop and state the missing user action.
