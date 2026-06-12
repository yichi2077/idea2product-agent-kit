# Pipeline Architecture

`.pipeline/vendor` is the audited source of active third-party skills. `.agents/skills` is a host discovery layer mapped from vendored skills and local custom skills.

Recipes in `.pipeline/recipes` are closed lists. Each recipe names explicit `$skill` calls and required outputs. All active skills carry `agents/openai.yaml` with implicit invocation disabled.

State lives under `.pipeline/state`. Do not directly modify gate approval fields. Phase completion hashes and reopen records live in `.pipeline/state/phase-metadata.json`; the state YAML remains the human-readable phase/gate surface.

## User-Level Entry Skills

The user-level Codex skill set lives in `$HOME/.agents/skills` and provides explicit call points:

- `idea2product-p0-guided-flow`: guided orchestrator.
- `idea2product-p1-idea-expansion` through `idea2product-p9-outcome-review`: explicit numbered phase skills.
- `idea2product-p0-status`: read-only state reporting.
- `idea2product-p0-resume`: continue from current state.

These entry skills call the repository pipeline commands instead of duplicating state logic.

## Agent Portability

The repository also ships `agent-adapters/` for non-Codex hosts. All adapters point back to the same `.pipeline` command surface and state files. Host-specific files should stay thin:

- Cursor: `.cursor/rules/idea2product.mdc`
- Claude Code: `CLAUDE.md`
- OpenCode: `.opencode/agents/idea2product.md`
- Hermes: `AGENTS.md` plus AgentSkills-compatible skills
- OpenClaw: `AGENTS.md`, `SOUL.md`, `TOOLS.md`, and workspace skills
- Generic: `AGENTS.md`

Do not fork pipeline state logic into host adapters.

## Closed-Loop State

`pipeline stage complete Px` records hashes for that phase's declared recipe outputs. `pipeline status` and `pipeline next` compare those hashes against current files and warn when a completed output is stale.

`pipeline reopen Px --reason "..."` is the supported rework path. It resets the target phase and downstream phases, clears affected gates, appends the reason to the decision log, and removes stale downstream phase metadata.

Gate requests enforce minimum evidence preconditions. Product Gate requires both the PRD and PM critic report to be real artifacts. Strategy Gate requires the decision memo, plus the red-team report in standard/high-assurance mode.
