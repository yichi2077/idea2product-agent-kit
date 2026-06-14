from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSUMPTIONS = ROOT / ".pipeline/state/assumption-register.yaml"
RISKS = ROOT / ".pipeline/state/risk-register.yaml"

def read_items(path: Path, label: str) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    items = []
    current = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- id:"):
            if current:
                items.append(current)
            current = {"kind": label, "id": stripped.split(":", 1)[1].strip().strip('"')}
        elif current and "review_by:" in stripped:
            current["review_by"] = stripped.split(":", 1)[1].strip().strip('"')
        elif current and "statement:" in stripped:
            current["statement"] = stripped.split(":", 1)[1].strip().strip('"')
        elif current and "status:" in stripped:
            current["status"] = stripped.split(":", 1)[1].strip().strip('"')
    if current:
        items.append(current)
    return items

def main() -> int:
    today = date.today().isoformat()
    due = read_items(ASSUMPTIONS, "assumption") + read_items(RISKS, "risk")
    matches = [
        item for item in due
        if item.get("status", "open") == "open" and item.get("review_by", "9999-99-99") <= today
    ]
    if not matches:
        print("No assumptions or risks due.")
        return 0
    for item in matches:
        print(f"{item.get('kind')} {item.get('id')}: due {item.get('review_by')} - {item.get('statement')}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
