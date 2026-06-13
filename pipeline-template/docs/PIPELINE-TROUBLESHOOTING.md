# Pipeline Troubleshooting

- If `pipeline run P2` is blocked, add a real `docs/00-idea/idea-brief.md`.
- If a gate approval fails, run it from a normal interactive terminal, not from Codex shell, CI, a pipe, or redirect.
- If phase skills are not available, run `python3 .pipeline/scripts/link_skills.py` from the project root and restart the agent session.
- If a vendored skill is missing expected context, inspect its `SOURCE.yaml` and `SKILL.md` under `.pipeline/vendor/`.
