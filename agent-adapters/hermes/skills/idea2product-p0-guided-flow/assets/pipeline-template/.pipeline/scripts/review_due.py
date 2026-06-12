from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / ".pipeline/state/assumption-register.yaml"

def main() -> int:
    text = REGISTER.read_text(encoding="utf-8")
    due = []
    current = {}
    for line in text.splitlines():
        if line.strip().startswith("- id:"):
            if current:
                due.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif "review_by:" in line:
            current["review_by"] = line.split(":", 1)[1].strip().strip('"')
        elif "statement:" in line:
            current["statement"] = line.split(":", 1)[1].strip().strip('"')
    if current:
        due.append(current)
    today = date.today().isoformat()
    matches = [item for item in due if item.get("review_by", "9999-99-99") <= today]
    if not matches:
        print("No assumptions due.")
        return 0
    for item in matches:
        print(f"{item.get('id')}: due {item.get('review_by')} - {item.get('statement')}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
