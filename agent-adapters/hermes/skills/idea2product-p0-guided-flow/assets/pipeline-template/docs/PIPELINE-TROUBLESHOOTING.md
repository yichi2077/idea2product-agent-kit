# Pipeline Troubleshooting

- If `pipeline run P2` is blocked, add a real `docs/00-idea/idea-brief.md`.
- If a gate approval fails, run it from a normal interactive terminal, not from Codex shell, CI, a pipe, or redirect.
- If skill audit fails, verify each active skill has `SKILL.md` and `agents/openai.yaml`.
- If vendor paths change upstream, update `SOURCE.yaml` and rerun verification.
