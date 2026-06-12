from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
bad = []
for skill in (ROOT / ".agents/skills").iterdir():
    if not (skill / "SKILL.md").exists():
        bad.append(str(skill))
    policy = skill / "agents/openai.yaml"
    if not policy.exists() or "allow_implicit_invocation: false" not in policy.read_text(encoding="utf-8"):
        bad.append(str(policy))
if bad:
    print("\n".join(bad))
    raise SystemExit(1)
print("Skill audit passed.")
