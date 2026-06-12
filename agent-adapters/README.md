# Agent Adapters

These adapters make the same idea2product pipeline usable from multiple coding agents. The shared `.pipeline` state machine remains the source of truth; each adapter only teaches a host how to find and operate it.

Supported adapters:

- `codex`: Codex user skills plus project `.agents/skills`.
- `cursor`: Cursor project rules in `.cursor/rules`.
- `claude-code`: Claude Code project memory in `CLAUDE.md`.
- `opencode`: OpenCode `AGENTS.md` plus `.opencode/agents/idea2product.md`.
- `hermes`: Hermes `AGENTS.md` and AgentSkills-compatible skills.
- `openclaw`: OpenClaw bootstrap files plus AgentSkills-compatible skills.
- `generic`: agent-neutral `AGENTS.md` fallback.
