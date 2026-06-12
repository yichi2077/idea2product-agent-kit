$ErrorActionPreference = "Stop"
python .pipeline/scripts/link_skills.py
python .pipeline/scripts/audit_skills.py
python .pipeline/scripts/detect_trigger_conflicts.py
python .pipeline/scripts/validate_recipes.py
python .pipeline/scripts/validate_state.py
python -m pytest .pipeline/tests -q
