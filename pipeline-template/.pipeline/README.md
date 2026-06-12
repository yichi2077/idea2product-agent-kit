# Decision Delivery Pipeline

This is an agent-portable 9-phase Idea -> Strategy -> Product -> Architecture -> Delivery pipeline. Codex, Cursor, Claude Code, OpenCode, Hermes, OpenClaw, and generic AGENTS.md-compatible agents should all operate the same `.pipeline` command surface.

Use `python .pipeline/scripts/pipeline.py status` to inspect state, `next` to find the next phase, and `run Px` to print the closed recipe for a phase.

Gate approval is intentionally separate and must be done by a human in an interactive terminal with `.pipeline/scripts/pipeline_gate.py`.
