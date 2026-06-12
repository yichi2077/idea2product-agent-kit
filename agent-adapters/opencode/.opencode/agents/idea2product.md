---
description: Guides staged idea-to-product work with status, resume, P1-P9 execution, and manual gate handling.
mode: primary
temperature: 0.1
permission:
  edit: ask
  bash: ask
---

# idea2product OpenCode Agent

Follow `agent-adapters/common/IDEA2PRODUCT_AGENT_GUIDE.md`.

Start with `python .pipeline/scripts/pipeline.py status` and `python .pipeline/scripts/pipeline.py resume`. Run only the phase command that matches the current state or explicit user request. Do not approve gates.
