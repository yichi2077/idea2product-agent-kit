#!/usr/bin/env sh
set -eu
python .pipeline/scripts/audit_skills.py
python .pipeline/scripts/detect_trigger_conflicts.py
python .pipeline/scripts/validate_recipes.py
python -m pytest .pipeline/tests -q
