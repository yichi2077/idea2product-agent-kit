from __future__ import annotations

import argparse
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIPE = ROOT / ".pipeline"
STATE = PIPE / "state" / "pipeline-state.yaml"
IDEA_BRIEF = ROOT / "docs/00-idea/idea-brief.md"
PHASES = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"]
MODES = {"light", "standard", "high-assurance"}
GATES = {"strategy", "product", "architecture", "release"}
# A scaffolded placeholder idea-brief carries this marker. The real-idea guard
# treats any brief that still contains it as "not a real idea yet".
SCAFFOLD_MARKER = "idea2product:scaffold-placeholder"

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")

def has_real_idea() -> bool:
    """True only when a real idea-brief exists: present, past the scaffold
    placeholder marker, and with non-trivial content."""
    if not IDEA_BRIEF.exists():
        return False
    text = IDEA_BRIEF.read_text(encoding="utf-8")
    if SCAFFOLD_MARKER in text:
        return False
    meaningful = [
        line for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    return len("\n".join(meaningful).strip()) >= 80

def status(_: argparse.Namespace) -> int:
    print(read(STATE))
    if not has_real_idea():
        print("\nNote: no real idea-brief yet. P2/P3 stay blocked until "
              "docs/00-idea/idea-brief.md holds a real idea.")
    return 0

def next_cmd(_: argparse.Namespace) -> int:
    state = read(STATE)
    for phase in PHASES:
        marker = f"  {phase}: ready"
        if marker in state:
            print(f"Next: run {phase}")
            print(f"Command: python .pipeline/scripts/pipeline.py run {phase}")
            return 0
    if "blocked_until_real_idea" in state:
        print("Blocked: capture a real idea in docs/00-idea/idea-brief.md, then "
              "complete P1.")
        return 1
    print("No phase is ready. Check gates or pending real idea.")
    return 1

def resume(_: argparse.Namespace) -> int:
    print("Pipeline status:")
    print(read(STATE))
    print("\nResume recommendation:")
    return next_cmd(argparse.Namespace())

def run_phase(args: argparse.Namespace) -> int:
    phase = args.phase.upper()
    recipe = next((PIPE / "recipes").glob(f"{phase.lower()}-*.yaml"), None)
    if not recipe:
        print(f"Unknown phase: {phase}")
        return 2
    print(f"Recipe: {recipe.relative_to(ROOT)}")
    print(read(recipe))
    if phase in {"P2", "P3"} and not has_real_idea():
        print("BLOCKED: docs/00-idea/idea-brief.md must hold a real idea "
              "(not the scaffold placeholder) before P2/P3.")
        return 3
    return 0

def reset_gate_fields(block: str) -> str:
    for key in ("approved_at", "approver", "commit", "tag"):
        block = re.sub(rf'{key}: (null|"[^"]*")', f"{key}: null", block, count=1)
    return block

def gate_request(args: argparse.Namespace) -> int:
    gate = args.gate.lower()
    if gate not in GATES:
        print(f"Unknown gate: {gate}")
        return 2
    challenge = secrets.token_hex(3).upper()
    text = read(STATE)
    pattern = re.compile(rf"(  {gate}:\n(?:    .+\n)+?)(?=  \w+:\n|phases:|\Z)")
    match = pattern.search(text)
    if not match:
        print(f"Gate block not found: {gate}")
        return 2
    block = match.group(1)
    if 'status: "approved"' in block:
        print(f"Gate already approved: {gate}")
        return 1
    block = re.sub(r'status: "[^"]+"', 'status: "awaiting_approval"', block, count=1)
    block = re.sub(r'requested_at: (null|"[^"]*")', f'requested_at: "{now()}"', block, count=1)
    block = re.sub(r'challenge: (null|"[^"]*")', f'challenge: "{challenge}"', block, count=1)
    block = reset_gate_fields(block)
    text = text[: match.start(1)] + block + text[match.end(1):]
    write(STATE, text)
    print(f"Gate requested: {gate}")
    print(f"Manual approval challenge: {challenge}")
    print("Approval must be performed by a human in a real interactive terminal using pipeline_gate.py.")
    return 0

def replace_phase_status(text: str, phase: str, status_value: str) -> str:
    pattern = re.compile(rf"(  {phase}: )\S+")
    if not pattern.search(text):
        raise ValueError(f"Phase status not found: {phase}")
    return pattern.sub(rf"\1{status_value}", text, count=1)

def replace_current_phase(text: str, phase: str) -> str:
    return re.sub(r'current_phase: "[^"]+"', f'current_phase: "{phase}"', text, count=1)

def replace_last_updated(text: str) -> str:
    return re.sub(r'last_updated: "[^"]+"', f'last_updated: "{now()}"', text, count=1)

def mode_set(args: argparse.Namespace) -> int:
    mode = args.mode.lower()
    if mode not in MODES:
        print(f"Unknown mode: {mode}. Choose one of: {', '.join(sorted(MODES))}")
        return 2
    text = read(STATE)
    if not re.search(r'mode: "[^"]*"', text):
        print("mode field not found in state.")
        return 2
    text = re.sub(r'mode: "[^"]*"', f'mode: "{mode}"', text, count=1)
    text = replace_last_updated(text)
    write(STATE, text)
    print(f"Mode set: {mode}")
    return 0

def stage_complete(args: argparse.Namespace) -> int:
    phase = args.phase.upper()
    if phase not in PHASES:
        print(f"Unknown phase: {phase}")
        return 2
    next_phase = PHASES[PHASES.index(phase) + 1] if phase != PHASES[-1] else None
    blocked_next = {
        "P3": "blocked_until_strategy_gate",
        "P5": "blocked_until_product_gate",
        "P6": "blocked_until_architecture_gate",
        "P8": "blocked_until_release_gate",
    }
    text = read(STATE)
    text = replace_phase_status(text, phase, "complete")
    if next_phase:
        if phase == "P1" and not has_real_idea():
            next_status = "blocked_until_real_idea"
        else:
            next_status = blocked_next.get(phase, "ready")
        text = replace_phase_status(text, next_phase, next_status)
        text = replace_current_phase(text, next_phase)
    text = replace_last_updated(text)
    write(STATE, text)
    print(f"Stage completed: {phase}")
    if next_phase:
        print(f"Next phase: {next_phase}")
        if phase == "P1" and not has_real_idea():
            print("P2 is blocked until docs/00-idea/idea-brief.md holds a real idea.")
    if phase in {"P3", "P5", "P6", "P8"}:
        gate = {"P3": "strategy", "P5": "product", "P6": "architecture", "P8": "release"}[phase]
        print(f"Required next gate command: python .pipeline/scripts/pipeline.py gate request {gate}")
    return 0

def assumptions_due(_: argparse.Namespace) -> int:
    return subprocess.call([sys.executable, str(PIPE / "scripts" / "review_due.py")])

def main() -> int:
    parser = argparse.ArgumentParser(prog="pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(func=status)
    sub.add_parser("next").set_defaults(func=next_cmd)
    sub.add_parser("resume").set_defaults(func=resume)
    run = sub.add_parser("run")
    run.add_argument("phase")
    run.set_defaults(func=run_phase)
    mode = sub.add_parser("mode")
    mode_sub = mode.add_subparsers(dest="mode_cmd", required=True)
    mode_set_p = mode_sub.add_parser("set")
    mode_set_p.add_argument("mode")
    mode_set_p.set_defaults(func=mode_set)
    stage = sub.add_parser("stage")
    stage_sub = stage.add_subparsers(dest="stage_cmd", required=True)
    complete = stage_sub.add_parser("complete")
    complete.add_argument("phase")
    complete.set_defaults(func=stage_complete)
    gate = sub.add_parser("gate")
    gate_sub = gate.add_subparsers(dest="gate_cmd", required=True)
    req = gate_sub.add_parser("request")
    req.add_argument("gate")
    req.set_defaults(func=gate_request)
    ass = sub.add_parser("assumptions")
    ass_sub = ass.add_subparsers(dest="ass_cmd", required=True)
    ass_due = ass_sub.add_parser("due")
    ass_due.set_defaults(func=assumptions_due)
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
