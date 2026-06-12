# Package Contents

- `skills/` — 12 installable entry skills (guided flow, P1–P9, status, resume).
- `pipeline-template/` — the repo-local `.pipeline` engine, `docs/` tree, recipes,
  templates, vendored domain skills, state registers, CI, and tests. Excludes
  `.pipeline/upstream`, `.git`, and local caches.
- `agent-adapters/` — host wiring for Claude Code, Codex, Cursor, OpenCode, Hermes,
  OpenClaw, and generic AGENTS.md agents. Hermes/OpenClaw embed a full mirror of
  `skills/`.
- `scripts/` — `install_user_skills.ps1`, `install_agent_adapters.ps1`,
  `scaffold_into_repo.ps1`, and `sync_bundles.py` (mirror/drift control).

Canonical sources: `pipeline-template/` and `skills/`. Run
`python scripts/sync_bundles.py --check` to confirm mirrors are in sync.
