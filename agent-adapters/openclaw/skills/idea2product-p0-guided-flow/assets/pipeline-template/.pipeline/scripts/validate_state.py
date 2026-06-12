from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".pipeline/state/pipeline-state.yaml"
GATE_PHASES = {"strategy": "P3", "product": "P5", "architecture": "P6", "release": "P8"}


def gate_block(text: str, gate: str) -> str | None:
    pattern = re.compile(rf"(  {gate}:\n(?:    .+\n)+?)(?=  \w+:\n|phases:|\Z)")
    match = pattern.search(text)
    return match.group(1) if match else None


def field(block: str, key: str) -> str | None:
    match = re.search(rf'{key}: (null|"([^"]*)")', block)
    if not match or match.group(1) == "null":
        return None
    return match.group(2)


def phase_status(text: str, phase: str) -> str | None:
    match = re.search(rf"  {phase}: (\S+)", text)
    return match.group(1) if match else None


def main() -> int:
    text = STATE.read_text(encoding="utf-8")
    errors = []
    for gate, phase in GATE_PHASES.items():
        block = gate_block(text, gate)
        if block is None:
            errors.append(f"missing gate block: {gate}")
            continue
        status = field(block, "status")
        if status in {"awaiting_approval", "approved"} and phase_status(text, phase) != "complete":
            errors.append(f"{gate} gate is {status} but {phase} is not complete")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("State validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
