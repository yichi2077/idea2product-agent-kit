# Decision Log

## 2026-06-12T11:06:22Z - Pipeline scaffold deployed

Decision: deploy Codex-only v3.1 pipeline with explicit recipe invocation, disabled implicit skill invocation, manual gates, and pending pilot until a real idea is supplied.

## 2026-06-12 - Expand to multi-agent portability

Decision: keep `.pipeline` as the single source of truth and add thin adapters for Codex, Cursor, Claude Code, OpenCode, Hermes, OpenClaw, and generic AGENTS.md-compatible agents. Adapters must call the shared pipeline commands instead of duplicating state logic.
