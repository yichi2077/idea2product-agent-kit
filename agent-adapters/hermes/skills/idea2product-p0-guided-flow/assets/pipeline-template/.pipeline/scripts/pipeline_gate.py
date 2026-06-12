from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".pipeline/state/pipeline-state.yaml"
METADATA = ROOT / ".pipeline/state/phase-metadata.json"
GATES = {"strategy", "product", "architecture", "release"}

# Environment markers that indicate a non-interactive automation host. The TTY
# check below is the primary defense; these provide defense in depth so the
# command refuses early with a clear message inside known agent runtimes.
NONHUMAN_ENV_MARKERS = (
    "CI",
    "GITHUB_ACTIONS",
    "GITLAB_CI",
    "BUILDKITE",
    "TF_BUILD",
    "CODEX",
    "CODEX_SANDBOX",
    "CODEX_PROXY_CERT",
    "CLAUDE_CODE",
    "CLAUDECODE",
    "ANTHROPIC_AGENT",
)


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_state(text: str) -> None:
    with STATE.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def mark_pilot_strategy_approved(text: str, gate: str) -> str:
    if gate != "strategy":
        return text
    return re.sub(
        r'pilot_validation: "P1_P3_AWAITING_STRATEGY_APPROVAL"',
        'pilot_validation: "P1_P3_STRATEGY_GATE_APPROVED"',
        text,
        count=1,
    )


def deny_nonhuman() -> None:
    for marker in NONHUMAN_ENV_MARKERS:
        if os.environ.get(marker):
            raise SystemExit(f"DENIED: gate approval is disabled in non-interactive host (env: {marker}).")
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise SystemExit("DENIED: gate approval requires a real interactive TTY.")


def gate_block_pattern(gate: str) -> re.Pattern[str]:
    return re.compile(rf"(  {gate}:\n(?:    .+\n)+?)(?=  \w+:\n|phases:|\Z)")


def find_block(text: str, gate: str) -> tuple[re.Match[str], str]:
    match = gate_block_pattern(gate).search(text)
    if not match:
        raise SystemExit(f"Gate block not found: {gate}")
    return match, match.group(1)


def field(block: str, key: str) -> str | None:
    match = re.search(rf"{key}: (null|\"([^\"]*)\")", block)
    if not match or match.group(1) == "null":
        return None
    return match.group(2)


def load_gate_confidence(gate: str) -> dict:
    if not METADATA.exists():
        return {}
    try:
        data = json.loads(METADATA.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    entry = data.get("gate_confidence", {}).get(gate)
    return entry if isinstance(entry, dict) else {}


def print_confidence_banner(gate: str) -> None:
    """Surface the agent's self-rated confidence so the approver can vary
    scrutiny. Absence is treated as a caution, not a pass."""
    entry = load_gate_confidence(gate)
    level = entry.get("level", "unstated")
    rationale = entry.get("rationale", "")
    print(f"Agent-stated confidence in this gate's decision context: {level.upper()}")
    if rationale:
        print(f"Confidence rationale: {rationale}")
    if level in {"low", "unstated"}:
        print(
            f"CAUTION: confidence is {level.upper()} -- review the prepared artifacts "
            "and the open assumptions/risks (pipeline.py handoff) with extra scrutiny "
            "before approving."
        )


def head_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def create_tag(gate: str, stamp: str, approver: str, note: str) -> str | None:
    """Create an annotated tag recording the approval. Returns the tag name or
    None when the repository has no commit to tag."""
    if head_commit() is None:
        return None
    safe_stamp = stamp.replace(":", "").replace("-", "")
    tag = f"i2p-gate-{gate}-{safe_stamp}"
    message = f"{gate} gate approved by {approver} at {stamp}\n\n{note}"
    result = subprocess.run(
        ["git", "tag", "-a", tag, "-m", message],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(f"Warning: could not create git tag ({result.stderr.strip()}).")
        return None
    return tag


def require_gate(gate: str) -> str:
    gate = gate.lower()
    if gate not in GATES:
        raise SystemExit(f"Unknown gate: {gate}")
    return gate


def prompt_human(gate: str, stored_challenge: str | None) -> tuple[bool, str]:
    """Collect and verify human confirmation. Returns (ok, note)."""
    if not stored_challenge:
        print("No challenge is recorded for this gate. Request the gate first.")
        return False, ""
    typed_gate = input("Type gate name: ").strip().lower()
    typed_challenge = input("Type challenge: ").strip().upper()
    note = input("Approval note: ").strip()
    if typed_gate != gate:
        print("Failed: gate name did not match.")
        return False, note
    if typed_challenge != stored_challenge.upper():
        print("Failed: challenge did not match the value issued at request time.")
        return False, note
    if not note:
        print("Failed: a non-empty approval note is required.")
        return False, note
    return True, note


def approve(args: argparse.Namespace) -> int:
    deny_nonhuman()
    gate = require_gate(args.gate)
    text = STATE.read_text(encoding="utf-8")
    match, block = find_block(text, gate)
    if 'status: "awaiting_approval"' not in block:
        print("Gate is not awaiting approval. Request the gate first.")
        return 2
    print_confidence_banner(gate)
    stored_challenge = field(block, "challenge")
    ok, note = prompt_human(gate, stored_challenge)
    if not ok:
        return 3
    stamp = now()
    approver = getpass.getuser()
    commit = head_commit() or "(no commit)"
    tag = create_tag(gate, stamp, approver, note)
    block = block.replace('status: "awaiting_approval"', 'status: "approved"', 1)
    block = re.sub(r"approved_at: (null|\"[^\"]*\")", f'approved_at: "{stamp}"', block, count=1)
    block = re.sub(r"approver: (null|\"[^\"]*\")", f'approver: "{approver}"', block, count=1)
    block = re.sub(r"commit: (null|\"[^\"]*\")", f'commit: "{commit}"', block, count=1)
    if "tag:" in block:
        block = re.sub(r"tag: (null|\"[^\"]*\")", f'tag: "{tag or ""}"', block, count=1)
    text = text[: match.start(1)] + block + text[match.end(1):]
    text = mark_pilot_strategy_approved(text, gate)
    write_state(text)
    log_decision(gate, "approved", stamp, approver, commit, tag, note)
    print(f"Approved {gate} gate at {stamp}.")
    if tag:
        print(f"Recorded approval tag: {tag}")
    else:
        print("No git commit was present, so no approval tag was created.")
    return 0


def reject(args: argparse.Namespace) -> int:
    deny_nonhuman()
    gate = require_gate(args.gate)
    text = STATE.read_text(encoding="utf-8")
    match, block = find_block(text, gate)
    if 'status: "awaiting_approval"' not in block:
        print("Gate is not awaiting approval. Nothing to reject.")
        return 2
    print_confidence_banner(gate)
    stored_challenge = field(block, "challenge")
    ok, note = prompt_human(gate, stored_challenge)
    if not ok:
        return 3
    stamp = now()
    approver = getpass.getuser()
    commit = head_commit() or "(no commit)"
    block = block.replace('status: "awaiting_approval"', 'status: "rejected"', 1)
    block = re.sub(r"approved_at: (null|\"[^\"]*\")", f'approved_at: "{stamp}"', block, count=1)
    block = re.sub(r"approver: (null|\"[^\"]*\")", f'approver: "{approver}"', block, count=1)
    text = text[: match.start(1)] + block + text[match.end(1):]
    write_state(text)
    log_decision(gate, "rejected", stamp, approver, commit, None, note)
    print(f"Rejected {gate} gate at {stamp}.")
    print("Address the recorded reason, then request the gate again to re-open it.")
    return 0


def log_decision(
    gate: str,
    action: str,
    stamp: str,
    approver: str,
    commit: str,
    tag: str | None,
    note: str,
) -> None:
    log = ROOT / ".pipeline/state/decision-log.md"
    tag_line = f"Tag: {tag}\n" if tag else ""
    with log.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(
            f"\n## {stamp} - {gate} gate {action}\n\n"
            f"Approver: {approver}\nCommit: {commit}\n{tag_line}Note: {note}\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(prog="pipeline_gate")
    sub = parser.add_subparsers(dest="cmd", required=True)
    app = sub.add_parser("approve")
    app.add_argument("gate")
    app.set_defaults(func=approve)
    rej = sub.add_parser("reject")
    rej.add_argument("gate")
    rej.set_defaults(func=reject)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
