#!/usr/bin/env sh
set -eu
# Prefer python3 -- the only interpreter name guaranteed on stock macOS and most
# modern Linux distros -- and fall back to python where only that name exists.
# Override explicitly with PYTHON=/path/to/interpreter if needed.
if [ -n "${PYTHON:-}" ]; then
  PY="$PYTHON"
elif command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "verify.sh: no python3 or python interpreter found on PATH." >&2
  exit 1
fi
"$PY" .pipeline/scripts/link_skills.py
"$PY" .pipeline/scripts/audit_skills.py
"$PY" .pipeline/scripts/detect_trigger_conflicts.py
"$PY" .pipeline/scripts/validate_recipes.py
"$PY" .pipeline/scripts/validate_state.py
"$PY" -m pytest .pipeline/tests -q
