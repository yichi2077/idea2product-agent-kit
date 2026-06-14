# Package Contents

- `skills/` — 16 installable entry skills (guided flow, P1–P9, P2 existing-solutions scan, status, resume, rollback, doctor, retire).
- `pipeline-template/` — the repo-local `.pipeline` engine, `docs/` tree, recipes,
  templates, vendored domain skills, state registers, and user-facing pipeline
  guides. Excludes internal dogfood/audit artifacts, `.pipeline/upstream`, `.git`,
  and local caches.
- `agent-adapters/` — host wiring for Claude Code, Codex, Cursor, OpenCode, Hermes,
  OpenClaw, and generic AGENTS.md agents. Hermes/OpenClaw embed a full mirror of
  `skills/`.
- `scripts/` — `install.py` plus Windows wrappers for user skill install, adapter
  install, and repo scaffolding.
