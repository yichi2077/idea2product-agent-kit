from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover - fallback path for minimal environments
    yaml = None


ROOT = Path(__file__).resolve().parents[2]
RECIPES = ROOT / ".pipeline" / "recipes"
SKILLS = ROOT / ".agents" / "skills"
EXPECTED_PHASES = {f"P{i}" for i in range(1, 10)}
ALLOWED_EXTERNAL_TOOLS = {
    "Context7 CLI",
    "speckit.specify",
    "speckit.clarify",
    "speckit.checklist",
    "speckit.plan",
    "speckit.tasks",
    "speckit.analyze",
}


def load_recipe(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required to validate recipe YAML.")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("recipe must be a YAML mapping")
    return data


def require_list(data: dict, key: str) -> list:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    return value


def optional_list(data: dict, key: str) -> list:
    value = data.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list when present")
    return value


def validate_skill_ref(item: str) -> None:
    if not isinstance(item, str) or not item.startswith("$"):
        raise ValueError(f"invalid skill reference: {item!r}")
    skill_name = item[1:]
    skill_path = SKILLS / skill_name / "SKILL.md"
    if not skill_path.exists():
        raise ValueError(f"missing active skill for {item}: {skill_path}")


def validate_conditional_skill(item: object, key: str) -> None:
    if not isinstance(item, dict):
        raise ValueError(f"{key} entries must be mappings")
    validate_skill_ref(item.get("name"))
    when = item.get("when")
    if not isinstance(when, str) or not when.strip():
        raise ValueError(f"{key} entries require a non-empty when field")


def validate_recipe(path: Path) -> str:
    data = load_recipe(path)
    phase = data.get("phase")
    if phase not in EXPECTED_PHASES:
        raise ValueError("phase must be one of P1..P9")
    if not path.name.startswith(phase.lower() + "-"):
        raise ValueError(f"filename must start with {phase.lower()}-")

    required_skills = optional_list(data, "required_skills")
    conditional_skills = optional_list(data, "conditional_skills")
    optional_skills = optional_list(data, "optional_skills")
    external_tools = optional_list(data, "external_tools")
    if "skills" in data:
        raise ValueError("use required_skills/conditional_skills/optional_skills instead of skills")
    if not required_skills and not external_tools:
        raise ValueError("recipe must define required_skills or external_tools")
    for item in required_skills:
        validate_skill_ref(item)
    for item in conditional_skills:
        validate_conditional_skill(item, "conditional_skills")
    for item in optional_skills:
        validate_conditional_skill(item, "optional_skills")

    for item in require_list(data, "required_context"):
        if not isinstance(item, str):
            raise ValueError("required_context entries must be strings")

    for item in require_list(data, "outputs"):
        if not isinstance(item, str):
            raise ValueError("outputs entries must be strings")

    unknown = [tool for tool in external_tools if tool not in ALLOWED_EXTERNAL_TOOLS]
    if unknown:
        raise ValueError(f"unknown external_tools: {unknown}")

    for key in ("non_skill_process", "completion_commands"):
        for item in optional_list(data, key):
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"{key} entries must be non-empty strings")

    verification = data.get("post_skill_verification")
    if not isinstance(verification, dict):
        raise ValueError("post_skill_verification must be a mapping")
    if verification.get("required") is not True:
        raise ValueError("post_skill_verification.required must be true")
    if not verification.get("fallback"):
        raise ValueError("post_skill_verification.fallback is required")
    return phase


def main() -> int:
    if yaml is None:
        print(
            "PyYAML is required for recipe validation. Install it with:\n"
            "  python -m pip install pyyaml\n"
            "(Only needed for verify/CI; the pipeline commands themselves do not require it.)",
            file=sys.stderr,
        )
        return 2
    errors: list[str] = []
    phases: list[str] = []
    for path in sorted(RECIPES.glob("p*.yaml")):
        try:
            phases.append(validate_recipe(path))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    missing = sorted(EXPECTED_PHASES - set(phases))
    duplicates = sorted({phase for phase in phases if phases.count(phase) > 1})
    if missing:
        errors.append(f"missing recipes for phases: {', '.join(missing)}")
    if duplicates:
        errors.append(f"duplicate recipes for phases: {', '.join(duplicates)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Recipe validation passed: {len(phases)} recipes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
