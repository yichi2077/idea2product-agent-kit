from __future__ import annotations

import argparse
import hashlib
import json
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIPE = ROOT / ".pipeline"
STATE = PIPE / "state" / "pipeline-state.yaml"
METADATA = PIPE / "state" / "phase-metadata.json"
IDEA_BRIEF = ROOT / "docs/00-idea/idea-brief.md"
ASSUMPTIONS = PIPE / "state" / "assumption-register.yaml"
RISKS = PIPE / "state" / "risk-register.yaml"
DECISION_LOG = PIPE / "state" / "decision-log.md"
PHASES = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"]
GATES = {"strategy", "product", "architecture", "release"}
GATE_PHASES = {"strategy": "P3", "product": "P5", "architecture": "P6", "release": "P8"}
CONFIDENCE_LEVELS = ("high", "medium", "low")
PYTHON_CMD = "python" if sys.platform.startswith("win") else "python3"
# A scaffolded placeholder idea-brief carries this marker. The real-idea guard
# treats any brief that still contains it as "not a real idea yet".
SCAFFOLD_MARKER = "idea2product:scaffold-placeholder"

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

def recipe_path(phase: str) -> Path | None:
    return next((PIPE / "recipes").glob(f"{phase.lower()}-*.yaml"), None)

def phase_outputs(phase: str) -> list[str]:
    recipe = recipe_path(phase)
    if not recipe:
        return []
    text = read(recipe)
    match = re.search(r"^outputs:\n((?:  - .+\n)+)", text, re.MULTILINE)
    if not match:
        return []
    outputs = []
    for line in match.group(1).splitlines():
        value = line.split("-", 1)[1].strip().strip('"')
        if value:
            outputs.append(value)
    return outputs

def load_metadata() -> dict:
    if not METADATA.exists():
        return {"phases": {}, "reopens": []}
    try:
        data = json.loads(read(METADATA))
    except json.JSONDecodeError:
        return {"phases": {}, "reopens": []}
    if not isinstance(data, dict):
        return {"phases": {}, "reopens": []}
    data.setdefault("phases", {})
    data.setdefault("reopens", [])
    return data

def save_metadata(data: dict) -> None:
    METADATA.parent.mkdir(parents=True, exist_ok=True)
    write(METADATA, json.dumps(data, indent=2, sort_keys=True) + "\n")

def file_sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

def is_scaffold_artifact(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return True
    text = path.read_text(encoding="utf-8", errors="replace")
    return "Status: scaffolded." in text or SCAFFOLD_MARKER in text

def record_phase_completion(phase: str, stamp: str) -> None:
    metadata = load_metadata()
    outputs = []
    for rel in phase_outputs(phase):
        outputs.append({"path": rel, "sha256": file_sha256(ROOT / rel)})
    metadata["phases"][phase] = {"completed_at": stamp, "outputs": outputs}
    save_metadata(metadata)

def stale_artifacts() -> list[tuple[str, str, str]]:
    metadata = load_metadata()
    stale = []
    for phase, info in metadata.get("phases", {}).items():
        if not isinstance(info, dict):
            continue
        for output in info.get("outputs", []):
            rel = output.get("path")
            old_hash = output.get("sha256")
            if not rel or not old_hash:
                continue
            current_hash = file_sha256(ROOT / rel)
            if current_hash != old_hash:
                stale.append((phase, rel, "missing" if current_hash is None else "changed"))
    return stale

def print_stale_warnings() -> None:
    stale = stale_artifacts()
    if not stale:
        return
    print("\nStale artifact warnings:")
    for phase, rel, status_value in stale:
        print(f"- {phase} output {rel} is {status_value}; reopen affected downstream phases if this changes approved decisions.")

def all_phases_complete(text: str) -> bool:
    return all(phase_status(text, phase) == "complete" for phase in PHASES)

def phase_status(text: str, phase: str) -> str | None:
    match = re.search(rf"  {phase}: (\S+)", text)
    return match.group(1) if match else None

def gate_block_pattern(gate: str) -> re.Pattern[str]:
    return re.compile(rf"(  {gate}:\n(?:    .+\n)+?)(?=  \w+:\n|phases:|\Z)")

def field(block: str, key: str) -> str | None:
    match = re.search(rf'{key}: (null|"([^"]*)")', block)
    if not match or match.group(1) == "null":
        return None
    return match.group(2)

def reset_gate_block(block: str) -> str:
    block = re.sub(r'status: "[^"]+"', 'status: "not_requested"', block, count=1)
    for key in ("requested_at", "approved_at", "approver", "challenge", "commit", "tag"):
        block = re.sub(rf'{key}: (null|"[^"]*")', f"{key}: null", block, count=1)
    return block

def reset_gate(text: str, gate: str) -> str:
    match = gate_block_pattern(gate).search(text)
    if not match:
        raise ValueError(f"Gate block not found: {gate}")
    block = reset_gate_block(match.group(1))
    return text[: match.start(1)] + block + text[match.end(1):]

def validate_state_invariants(text: str) -> list[str]:
    errors = []
    for gate, phase in GATE_PHASES.items():
        match = gate_block_pattern(gate).search(text)
        if not match:
            errors.append(f"missing gate block: {gate}")
            continue
        gate_status = field(match.group(1), "status")
        if gate_status in {"awaiting_approval", "approved"} and phase_status(text, phase) != "complete":
            errors.append(f"{gate} gate is {gate_status} but {phase} is not complete")
    seen_incomplete = False
    for phase in PHASES:
        status_value = phase_status(text, phase)
        if status_value != "complete":
            seen_incomplete = True
        elif seen_incomplete:
            errors.append(f"{phase} is complete but an earlier phase is not complete")
    return errors

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
    print_stale_warnings()
    return 0

def print_next_action(state: str) -> int:
    if all_phases_complete(state):
        print("Pipeline complete. Review outcomes, reopen a phase for rework, or retire/archive the project.")
        return 0
    for phase in PHASES:
        marker = f"  {phase}: ready"
        if marker in state:
            print(f"Next: run {phase}")
            print(f"Command: {PYTHON_CMD} .pipeline/scripts/pipeline.py run {phase}")
            return 0
    if re.search(r"  P\d: retired", state):
        print("Project retired. Run reopen <completed phase> to resume from a completed checkpoint.")
        return 1
    if "blocked_until_real_idea" in state:
        print("Blocked: capture a real idea in docs/00-idea/idea-brief.md, then "
              "complete P1.")
        return 1
    print("No phase is ready. Check gates or pending real idea.")
    return 1

def next_cmd(_: argparse.Namespace) -> int:
    state = read(STATE)
    print_stale_warnings()
    return print_next_action(state)

def resume(_: argparse.Namespace) -> int:
    print("Pipeline status:")
    state = read(STATE)
    print(state)
    print("\nResume recommendation:")
    rc = next_cmd(argparse.Namespace())
    if all_phases_complete(state):
        print("Outcome review is complete. Use handoff to inspect decisions, or reopen a completed phase if outcome evidence requires rework.")
    print("\nFor a full handoff brief (decisions, open assumptions, risks, staleness):")
    print(f"  {PYTHON_CMD} .pipeline/scripts/pipeline.py handoff")
    return rc

def read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

REGISTER_KEYS = {"statement", "status", "review_by", "severity", "owner", "mitigation"}

def parse_register(path: Path) -> list[dict]:
    """Parse the kit's lightweight ``- id:`` field registers without PyYAML.
    Only the known scalar field keys are captured; nested/list values are
    ignored so this stays a read-only summarizer, never a second source."""
    items: list[dict] = []
    current: dict = {}
    for line in read_optional(path).splitlines():
        stripped = line.strip()
        if stripped.startswith("- id:"):
            if current:
                items.append(current)
            current = {"id": stripped.split(":", 1)[1].strip().strip('"')}
        elif current and ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip().lstrip("-").strip()
            if key in REGISTER_KEYS:
                current[key] = value.strip().strip('"')
    if current:
        items.append(current)
    return items

def decision_headers() -> list[str]:
    return [line[3:].strip() for line in read_optional(DECISION_LOG).splitlines() if line.startswith("## ")]

def handoff(_: argparse.Namespace) -> int:
    """Read-only handoff brief: the five things a returning operator or a fresh
    agent session needs to avoid re-litigating settled work -- position, next
    step, gate state, decisions already made, open questions, and stale evidence.
    It only reads the registers the pipeline already maintains."""
    text = read(STATE)
    today = now()[:10]
    print("# idea2product handoff brief")
    current = re.search(r'current_phase: "([^"]+)"', text)
    if current:
        print(f"Current phase: {current.group(1)}")
    pilot = re.search(r'pilot_validation: "([^"]+)"', text)
    if pilot:
        print(f"Pilot validation: {pilot.group(1)}")
    print("\n## Next step")
    print_next_action(text)
    print("\n## Gates")
    for gate in ("strategy", "product", "architecture", "release"):
        match = gate_block_pattern(gate).search(text)
        gate_status = field(match.group(1), "status") if match else "unknown"
        print(f"- {gate}: {gate_status}")
    print("\n## Recent decisions (oldest to newest)")
    decisions = decision_headers()
    if decisions:
        for head in decisions[-5:]:
            print(f"- {head}")
    else:
        print("- none recorded")
    print("\n## Open assumptions")
    open_assumptions = [a for a in parse_register(ASSUMPTIONS) if a.get("status") == "open"]
    if open_assumptions:
        for assumption in open_assumptions:
            review_by = assumption.get("review_by", "?")
            overdue = " OVERDUE" if review_by != "?" and review_by <= today else ""
            print(f"- {assumption.get('id')} (review by {review_by}{overdue}): {assumption.get('statement', '')}")
    else:
        print("- none open")
    print("\n## Open risks")
    open_risks = [r for r in parse_register(RISKS) if r.get("status") == "open"]
    if open_risks:
        for risk in open_risks:
            review_by = risk.get("review_by")
            due = ""
            if review_by:
                due = f" (review by {review_by}{' OVERDUE' if review_by <= today else ''})"
            print(f"- {risk.get('id')} [{risk.get('severity', '?')}]{due}: {risk.get('statement', '')}")
    else:
        print("- none open")
    print_stale_warnings()
    return 0

def run_phase(args: argparse.Namespace) -> int:
    phase = args.phase.upper()
    recipe = recipe_path(phase)
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

def record_gate_confidence(gate: str, level: str | None, rationale: str | None) -> None:
    """Persist the agent's self-rated confidence in the prepared decision
    context to the metadata sidecar. It informs the human approver's scrutiny;
    it never auto-approves or auto-rejects (self-rated confidence is not a
    reliable gate)."""
    metadata = load_metadata()
    metadata.setdefault("gate_confidence", {})[gate] = {
        "level": level or "unstated",
        "rationale": (rationale or "").strip(),
        "recorded_at": now(),
    }
    save_metadata(metadata)

def gate_request(args: argparse.Namespace) -> int:
    gate = args.gate.lower()
    if gate not in GATES:
        print(f"Unknown gate: {gate}")
        return 2
    precondition_errors = gate_precondition_errors(gate)
    if precondition_errors:
        print(f"Gate preconditions failed for {gate}:")
        for error in precondition_errors:
            print(f"- {error}")
        return 3
    challenge = secrets.token_hex(3).upper()
    text = read(STATE)
    invariant_errors = validate_state_invariants(text)
    if invariant_errors:
        print("State invariant violation:")
        for error in invariant_errors:
            print(f"- {error}")
        return 4
    match = gate_block_pattern(gate).search(text)
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
    record_gate_confidence(gate, args.confidence, args.rationale)
    print(f"Gate requested: {gate}")
    print(f"Manual approval challenge: {challenge}")
    level = args.confidence or "unstated"
    print(f"Recorded agent confidence: {level}")
    if level in {"low", "unstated"}:
        print("Confidence is low/unstated; the human approver will be prompted to apply extra scrutiny.")
    print("Approval must be performed by a human in a real interactive terminal using pipeline_gate.py.")
    return 0

def gate_precondition_errors(gate: str) -> list[str]:
    text = read(STATE)
    errors = []
    gate_phase = GATE_PHASES[gate]
    if phase_status(text, gate_phase) != "complete":
        errors.append(
            f"{gate_phase} must be complete before requesting the {gate} gate; "
            f"run stage complete {gate_phase} (or reopen {gate_phase} if it was rolled back)."
        )
    if gate == "strategy":
        decision_memo = ROOT / "docs/10-strategy/decision-memo.md"
        if is_scaffold_artifact(decision_memo):
            errors.append("docs/10-strategy/decision-memo.md must exist and contain real decision evidence.")
        red_team = ROOT / ".pipeline/reports/strategy-red-team.md"
        if is_scaffold_artifact(red_team):
            errors.append(".pipeline/reports/strategy-red-team.md is required before the strategy gate.")
    if gate == "product":
        prd = ROOT / "docs/20-product/prd.md"
        critic = ROOT / "docs/20-product/pm-critic-report.md"
        if is_scaffold_artifact(prd):
            errors.append("docs/20-product/prd.md must exist and contain real PRD evidence.")
        if is_scaffold_artifact(critic):
            errors.append("docs/20-product/pm-critic-report.md must exist and contain a real fresh-context critic review.")
        metadata = load_metadata()
        p5 = metadata.get("phases", {}).get("P5", {})
        output_hashes = {item.get("path"): item.get("sha256") for item in p5.get("outputs", []) if isinstance(item, dict)}
        prd_hash = output_hashes.get("docs/20-product/prd.md")
        critic_hash = output_hashes.get("docs/20-product/pm-critic-report.md")
        if prd_hash and file_sha256(prd) != prd_hash:
            errors.append("docs/20-product/prd.md changed after P5 completion; rerun P5 or reopen before requesting Product Gate.")
        if critic_hash and file_sha256(critic) != critic_hash:
            errors.append("docs/20-product/pm-critic-report.md changed after P5 completion; rerun P5 or reopen before requesting Product Gate.")
    return errors

def output_candidates(rel: str) -> list[Path]:
    if "<feature>" in rel:
        return sorted(ROOT.glob(rel.replace("<feature>", "*")))
    return [ROOT / rel]

def phase_output_errors(phase: str) -> list[str]:
    errors = []
    if phase == "P1" and not has_real_idea():
        errors.append("docs/00-idea/idea-brief.md must hold a real idea before P1 can be completed.")
    for rel in phase_outputs(phase):
        candidates = output_candidates(rel)
        if not candidates or all(not candidate.exists() for candidate in candidates):
            errors.append(f"{rel} is required before {phase} can be completed.")
            continue
        files = [candidate for candidate in candidates if candidate.exists() and candidate.is_file()]
        if not files:
            errors.append(f"{rel} must resolve to at least one file before {phase} can be completed.")
            continue
        if all(is_scaffold_artifact(candidate) for candidate in files):
            errors.append(f"{rel} is still scaffolded; replace it with real phase evidence before completing {phase}.")
    return errors

def replace_phase_status(text: str, phase: str, status_value: str) -> str:
    pattern = re.compile(rf"(  {phase}: )\S+")
    if not pattern.search(text):
        raise ValueError(f"Phase status not found: {phase}")
    return pattern.sub(rf"\1{status_value}", text, count=1)

def replace_current_phase(text: str, phase: str) -> str:
    return re.sub(r'current_phase: "[^"]+"', f'current_phase: "{phase}"', text, count=1)

def replace_pilot_validation(text: str, status_value: str) -> str:
    return re.sub(r'pilot_validation: "[^"]+"', f'pilot_validation: "{status_value}"', text, count=1)

def replace_register_status(text: str, item_id: str, status_value: str) -> str:
    return re.sub(
        rf'(- id: {re.escape(item_id)}\n(?:    .+\n)*?    status: )"[^"]+"',
        rf'\1"{status_value}"',
        text,
        count=1,
    )

def close_real_idea_seed_registers() -> None:
    """Retire the scaffold's initial no-real-idea assumption/risk.

    These seed records are useful before P1, but once a real idea has passed the
    guard they become misleading handoff noise if the agent forgets to update
    the registers manually.
    """
    if ASSUMPTIONS.exists():
        text = read(ASSUMPTIONS)
        updated = replace_register_status(text, "A-0001", "closed")
        if updated != text:
            write(ASSUMPTIONS, updated)
    if RISKS.exists():
        text = read(RISKS)
        updated = replace_register_status(text, "R-0001", "closed")
        if updated != text:
            write(RISKS, updated)

def stage_complete(args: argparse.Namespace) -> int:
    phase = args.phase.upper()
    if phase not in PHASES:
        print(f"Unknown phase: {phase}")
        return 2
    text = read(STATE)
    current_status = phase_status(text, phase)
    if current_status != "ready":
        print(f"Stage completion blocked for {phase}:")
        print(f"- {phase} is {current_status}; only the current ready phase can be completed.")
        print_next_action(text)
        return 3
    output_errors = phase_output_errors(phase)
    if output_errors:
        print(f"Stage completion blocked for {phase}:")
        for error in output_errors:
            print(f"- {error}")
        return 3
    next_phase = PHASES[PHASES.index(phase) + 1] if phase != PHASES[-1] else None
    blocked_next = {
        "P3": "blocked_until_strategy_gate",
        "P5": "blocked_until_product_gate",
        "P6": "blocked_until_architecture_gate",
        "P8": "blocked_until_release_gate",
    }
    stamp = now()
    text = replace_phase_status(text, phase, "complete")
    if next_phase:
        next_status = blocked_next.get(phase, "ready")
        text = replace_phase_status(text, next_phase, next_status)
        text = replace_current_phase(text, next_phase)
    if phase == "P3" and has_real_idea():
        text = replace_pilot_validation(text, "P1_P3_AWAITING_STRATEGY_APPROVAL")
    text = re.sub(r'last_updated: "[^"]+"', f'last_updated: "{stamp}"', text, count=1)
    write(STATE, text)
    if phase == "P1" and has_real_idea():
        close_real_idea_seed_registers()
    record_phase_completion(phase, stamp)
    print(f"Stage completed: {phase}")
    if next_phase:
        print(f"Next phase: {next_phase}")
    if phase in {"P3", "P5", "P6", "P8"}:
        gate = {"P3": "strategy", "P5": "product", "P6": "architecture", "P8": "release"}[phase]
        print(f"Required next gate command: {PYTHON_CMD} .pipeline/scripts/pipeline.py gate request {gate}")
    return 0

def reopen(args: argparse.Namespace) -> int:
    phase = args.phase.upper()
    reason = (args.reason or "").strip()
    if phase not in PHASES:
        print(f"Unknown phase: {phase}")
        return 2
    if not reason:
        print("Reopen requires a non-empty --reason.")
        return 2
    text = read(STATE)
    current_status = phase_status(text, phase)
    if current_status != "complete":
        print(f"Cannot reopen {phase}: only a completed phase can be reopened "
              f"(current status: {current_status}).")
        return 2
    affected = PHASES[PHASES.index(phase):]
    text = replace_phase_status(text, phase, "ready")
    for downstream in affected[1:]:
        text = replace_phase_status(text, downstream, "waiting")
    text = replace_current_phase(text, phase)
    stamp = now()
    text = re.sub(r'last_updated: "[^"]+"', f'last_updated: "{stamp}"', text, count=1)
    if "P3" in affected:
        # Reopening any of P1-P3 unsettles the strategy decision; revoke an
        # awaiting/approved pilot claim instead of leaving it overstated. Re-running
        # stage complete P3 restores P1_P3_AWAITING_STRATEGY_APPROVAL.
        text = re.sub(
            r'pilot_validation: "(P1_P3_AWAITING_STRATEGY_APPROVAL|P1_P3_STRATEGY_GATE_APPROVED)"',
            'pilot_validation: "PENDING_REAL_IDEA"', text, count=1)
    for gate, gate_phase in GATE_PHASES.items():
        if gate_phase in affected:
            text = reset_gate(text, gate)
    write(STATE, text)
    metadata = load_metadata()
    for downstream in affected:
        metadata.get("phases", {}).pop(downstream, None)
    for gate, gate_phase in GATE_PHASES.items():
        if gate_phase in affected:
            metadata.get("gate_confidence", {}).pop(gate, None)
    metadata.setdefault("reopens", []).append({"phase": phase, "reopened_at": stamp, "reason": reason})
    save_metadata(metadata)
    log = PIPE / "state" / "decision-log.md"
    with log.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"\n## {stamp} - reopened {phase}\n\nReason: {reason}\nAffected phases: {', '.join(affected)}\n")
    print(f"Reopened {phase}: {reason}")
    print(f"Affected phases: {', '.join(affected)}")
    return 0

def assumptions_due(_: argparse.Namespace) -> int:
    return subprocess.call([sys.executable, str(PIPE / "scripts" / "review_due.py")])

def doctor(_: argparse.Namespace) -> int:
    issues: list[str] = []
    required_paths = [
        PIPE,
        PIPE / "scripts" / "pipeline.py",
        PIPE / "recipes",
        PIPE / "state",
        STATE,
        ASSUMPTIONS,
        RISKS,
        DECISION_LOG,
    ]
    for path in required_paths:
        if not path.exists():
            issues.append(f"missing required path: {path.relative_to(ROOT)}")
    for phase in PHASES:
        if recipe_path(phase) is None:
            issues.append(f"missing recipe for {phase}")
    if STATE.exists():
        text = read(STATE)
        issues.extend(validate_state_invariants(text))
        for phase in PHASES:
            if phase_status(text, phase) == "complete":
                issues.extend(phase_output_errors(phase))
        if not has_real_idea():
            for phase in ("P2", "P3"):
                status_value = phase_status(text, phase)
                if status_value not in {"blocked_until_real_idea", "waiting", "retired"}:
                    issues.append(f"{phase} is {status_value} but no real idea-brief exists")
    for register in (ASSUMPTIONS, RISKS):
        if register.exists():
            try:
                parse_register(register)
            except OSError as exc:
                issues.append(f"cannot read {register.relative_to(ROOT)}: {exc}")
    stale = stale_artifacts()
    for phase, rel, status_value in stale:
        issues.append(f"stale output: {phase} {rel} is {status_value}")
    if issues:
        print("Workspace doctor found issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("✓ healthy")
    return 0

def retire(args: argparse.Namespace) -> int:
    reason = args.reason.strip()
    if not reason:
        print("Retire requires a non-empty --reason.")
        return 2
    text = read(STATE)
    changed = []
    for phase in PHASES:
        if phase_status(text, phase) != "complete":
            text = replace_phase_status(text, phase, "retired")
            changed.append(phase)
    stamp = now()
    text = re.sub(r'last_updated: "[^"]+"', f'last_updated: "{stamp}"', text, count=1)
    write(STATE, text)
    with DECISION_LOG.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"\n## {stamp} - retired\n\nReason: {reason}\nRetired phases: {', '.join(changed) or 'none'}\n")
    print(f"Project retired: {reason}")
    if changed:
        print(f"Retired phases: {', '.join(changed)}")
    else:
        print("All phases were already complete; no phase statuses changed.")
    print("Run reopen <completed phase> to resume from a completed checkpoint.")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(prog="pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(func=status)
    sub.add_parser("next").set_defaults(func=next_cmd)
    sub.add_parser("resume").set_defaults(func=resume)
    sub.add_parser("handoff").set_defaults(func=handoff)
    sub.add_parser("doctor").set_defaults(func=doctor)
    run = sub.add_parser("run")
    run.add_argument("phase")
    run.set_defaults(func=run_phase)
    stage = sub.add_parser("stage")
    stage_sub = stage.add_subparsers(dest="stage_cmd", required=True)
    complete = stage_sub.add_parser("complete")
    complete.add_argument("phase")
    complete.set_defaults(func=stage_complete)
    gate = sub.add_parser("gate")
    gate_sub = gate.add_subparsers(dest="gate_cmd", required=True)
    req = gate_sub.add_parser("request")
    req.add_argument("gate")
    req.add_argument("--confidence", choices=CONFIDENCE_LEVELS,
                     help="agent self-rated confidence in the prepared decision context")
    req.add_argument("--rationale", help="what drives that confidence (ground it in open assumptions/risks)")
    req.set_defaults(func=gate_request)
    reopen_p = sub.add_parser("reopen")
    reopen_p.add_argument("phase")
    reopen_p.add_argument("--reason", required=True)
    reopen_p.set_defaults(func=reopen)
    retire_p = sub.add_parser("retire")
    retire_p.add_argument("--reason", required=True)
    retire_p.set_defaults(func=retire)
    ass = sub.add_parser("assumptions")
    ass_sub = ass.add_subparsers(dest="ass_cmd", required=True)
    ass_due = ass_sub.add_parser("due")
    ass_due.set_defaults(func=assumptions_due)
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
