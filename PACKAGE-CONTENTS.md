# Package Contents

- `skills/` — 16 installable entry skills (guided flow, P1-P10, status, resume, rollback, doctor, retire). P2 strategy analysis includes the existing-solutions scan as a required first step.
- `pipeline-template/` — the repo-local `.pipeline` engine, `docs/` tree, recipes,
  templates, vendored domain skills, state registers, and user-facing pipeline
  guides. Excludes internal dogfood/audit artifacts, `.pipeline/upstream`, `.git`,
  and local caches.
- `agent-adapters/` — host wiring for Claude Code, Codex, Cursor, OpenCode, Hermes,
  OpenClaw, and generic AGENTS.md agents. Hermes/OpenClaw embed a full mirror of
  `skills/`.
- `scripts/` — `install.py`, the cross-platform installer with `init` (one-shot
  onboarding), `skills`, `scaffold`, `adapters`, `upgrade`, and `speckit` subcommands;
  `sync_bundled_copies.py`, which keeps the bundled copies in sync; and optional
  Windows `.ps1` convenience wrappers.
