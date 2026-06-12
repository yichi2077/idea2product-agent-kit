import importlib.util
import json
import shutil
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def run(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)

def load_module(rel_path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def backup_state(tmp_path):
    state = ROOT / ".pipeline/state/pipeline-state.yaml"
    log = ROOT / ".pipeline/state/decision-log.md"
    metadata = ROOT / ".pipeline/state/phase-metadata.json"
    state_bak = tmp_path / "state.yaml"
    log_bak = tmp_path / "log.md"
    metadata_bak = tmp_path / "metadata.json"
    shutil.copy2(state, state_bak)
    if log.exists():
        shutil.copy2(log, log_bak)
    if metadata.exists():
        shutil.copy2(metadata, metadata_bak)
    return state, log, metadata, state_bak, log_bak, metadata_bak

def restore_state(state, log, metadata, state_bak, log_bak, metadata_bak):
    shutil.copy2(state_bak, state)
    if log_bak.exists():
        shutil.copy2(log_bak, log)
    if metadata_bak.exists():
        shutil.copy2(metadata_bak, metadata)
    elif metadata.exists():
        metadata.unlink()

def backup_paths(tmp_path, *paths):
    backups = []
    for path in paths:
        target = ROOT / path
        backup = tmp_path / path.replace("/", "__")
        if target.exists():
            shutil.copy2(target, backup)
        backups.append((target, backup))
    return backups

def restore_paths(backups):
    for target, backup in backups:
        if backup.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, target)
        elif target.exists():
            target.unlink()

def write_file(rel_path, text):
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def write_real_strategy_artifacts():
    write_file("docs/10-strategy/decision-memo.md", "# Decision Memo\n\nReal strategy decision evidence for test.\n")
    write_file(".pipeline/reports/strategy-red-team.md", "# Strategy Red Team\n\nReal red-team findings for test.\n")

def write_real_product_artifacts():
    write_file("docs/20-product/prd.md", "# PRD\n\nReal PRD evidence for test.\n")
    write_file("docs/20-product/pm-critic-report.md", "# PM Critic Report\n\nReal fresh-context critic review for test.\n")

def gate_block(text, gate):
    after = text.split(f"  {gate}:", 1)[1]
    for nxt in ("strategy", "product", "architecture", "release", "phases:"):
        if f"  {nxt}:" in after and nxt != gate:
            return after.split(f"  {nxt}:", 1)[0]
    return after

def test_status_command():
    result = run(".pipeline/scripts/pipeline.py", "status")
    assert result.returncode == 0
    assert "version: \"3.1\"" in result.stdout

def test_recipe_command_prints_closed_skill_list():
    result = run(".pipeline/scripts/pipeline.py", "run", "P1")
    assert result.returncode == 0
    assert "$assumption-challenger" in result.stdout

def test_recipes_validate_against_active_skills():
    result = run(".pipeline/scripts/validate_recipes.py")
    assert result.returncode == 0, result.stderr
    assert "Recipe validation passed: 9 recipes" in result.stdout

def test_resume_command_reports_next_action():
    result = run(".pipeline/scripts/pipeline.py", "resume")
    assert result.returncode == 0
    assert "Resume recommendation:" in result.stdout
    assert f"Command: {'python' if sys.platform.startswith('win') else 'python3'} .pipeline/scripts/pipeline.py run P1" in result.stdout

def test_handoff_brief_is_readonly_and_surfaces_decisions_assumptions_risks(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        before = state.read_text(encoding="utf-8")
        result = run(".pipeline/scripts/pipeline.py", "handoff")
        assert result.returncode == 0
        out = result.stdout
        assert "handoff brief" in out
        assert "## Next step" in out
        assert "## Gates" in out
        assert "## Recent decisions" in out
        assert "## Open assumptions" in out and "A-0001" in out
        assert "## Open risks" in out and "R-0001" in out
        # The brief is a read-only renderer; it must never mutate state.
        assert state.read_text(encoding="utf-8") == before
    finally:
        restore_state(state, log, metadata, sb, lb, mb)

def test_resume_points_to_handoff_brief():
    result = run(".pipeline/scripts/pipeline.py", "resume")
    assert result.returncode == 0
    assert "pipeline.py handoff" in result.stdout

def test_gate_request_updates_target_gate_only(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        # A gate can only be requested once its phase is complete, so finish P8
        # before exercising the release-gate request.
        assert run(".pipeline/scripts/pipeline.py", "stage", "complete", "P8").returncode == 0
        result = run(".pipeline/scripts/pipeline.py", "gate", "request", "release")
        assert result.returncode == 0
        text = state.read_text(encoding="utf-8")
        strategy_block = text.split("  strategy:", 1)[1].split("  product:", 1)[0]
        release_block = text.split("  release:", 1)[1].split("phases:", 1)[0]
        assert 'status: "not_requested"' in strategy_block
        assert 'requested_at: null' in strategy_block
        assert 'status: "awaiting_approval"' in release_block
        assert 'requested_at: "' in release_block
    finally:
        restore_state(state, log, metadata, sb, lb, mb)

def test_stage_complete_updates_phase_without_approving_gate(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        before_product_block = state.read_text(encoding="utf-8").split("  product:", 1)[1].split("  architecture:", 1)[0]
        result = run(".pipeline/scripts/pipeline.py", "stage", "complete", "P5")
        assert result.returncode == 0
        text = state.read_text(encoding="utf-8")
        assert "  P5: complete" in text
        assert "  P6: blocked_until_product_gate" in text
        product_block = text.split("  product:", 1)[1].split("  architecture:", 1)[0]
        assert product_block == before_product_block
        expected_python = "python" if sys.platform.startswith("win") else "python3"
        assert f"Required next gate command: {expected_python} .pipeline/scripts/pipeline.py gate request product" in result.stdout
    finally:
        restore_state(state, log, metadata, sb, lb, mb)

def test_gate_approval_denied_without_tty():
    result = run(".pipeline/scripts/pipeline_gate.py", "approve", "strategy")
    assert result.returncode != 0
    assert "DENIED" in (result.stderr + result.stdout)

def test_active_skills_have_disabled_implicit_invocation():
    for skill in (ROOT / ".agents/skills").iterdir():
        if skill.is_dir():
            policy = skill / "agents/openai.yaml"
            assert policy.exists(), skill
            assert "allow_implicit_invocation: false" in policy.read_text(encoding="utf-8")

def test_wrong_challenge_is_rejected(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    backups = backup_paths(tmp_path, "docs/10-strategy/decision-memo.md", ".pipeline/reports/strategy-red-team.md")
    try:
        write_real_strategy_artifacts()
        run(".pipeline/scripts/pipeline.py", "stage", "complete", "P3")
        run(".pipeline/scripts/pipeline.py", "gate", "request", "strategy")
        pg = load_module(".pipeline/scripts/pipeline_gate.py", "pg_wrong")
        pg.deny_nonhuman = lambda: None
        answers = iter(["strategy", "DEFINITELY-WRONG", "a note"])
        pg.input = lambda *a, **k: next(answers)
        rc = pg.approve(types.SimpleNamespace(gate="strategy"))
        assert rc == 3
        block = gate_block(state.read_text(encoding="utf-8"), "strategy")
        assert 'status: "awaiting_approval"' in block
        assert 'status: "approved"' not in block
    finally:
        restore_paths(backups)
        restore_state(state, log, metadata, sb, lb, mb)

def test_correct_challenge_approves(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    backups = backup_paths(tmp_path, "docs/00-idea/idea-brief.md", "docs/10-strategy/decision-memo.md", ".pipeline/reports/strategy-red-team.md")
    try:
        write_file("docs/00-idea/idea-brief.md", "# Idea\n\nThis is a real idea body long enough to satisfy the strategy pilot validation path during approval tests.\n")
        write_real_strategy_artifacts()
        run(".pipeline/scripts/pipeline.py", "stage", "complete", "P3")
        run(".pipeline/scripts/pipeline.py", "gate", "request", "strategy")
        block = gate_block(state.read_text(encoding="utf-8"), "strategy")
        challenge = block.split('challenge: "', 1)[1].split('"', 1)[0]
        pg = load_module(".pipeline/scripts/pipeline_gate.py", "pg_ok")
        pg.deny_nonhuman = lambda: None
        pg.create_tag = lambda *a, **k: None  # isolate test from git tag side effects
        answers = iter(["strategy", challenge, "approved for test"])
        pg.input = lambda *a, **k: next(answers)
        rc = pg.approve(types.SimpleNamespace(gate="strategy"))
        assert rc == 0
        text = state.read_text(encoding="utf-8")
        block = gate_block(text, "strategy")
        assert 'status: "approved"' in block
        assert 'pilot_validation: "P1_P3_STRATEGY_GATE_APPROVED"' in text
    finally:
        restore_paths(backups)
        restore_state(state, log, metadata, sb, lb, mb)

def test_gate_reject_sets_rejected(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    backups = backup_paths(tmp_path, "docs/10-strategy/decision-memo.md", ".pipeline/reports/strategy-red-team.md")
    try:
        write_real_strategy_artifacts()
        run(".pipeline/scripts/pipeline.py", "stage", "complete", "P3")
        run(".pipeline/scripts/pipeline.py", "gate", "request", "strategy")
        block = gate_block(state.read_text(encoding="utf-8"), "strategy")
        challenge = block.split('challenge: "', 1)[1].split('"', 1)[0]
        pg = load_module(".pipeline/scripts/pipeline_gate.py", "pg_rej")
        pg.deny_nonhuman = lambda: None
        answers = iter(["strategy", challenge, "rejecting for test"])
        pg.input = lambda *a, **k: next(answers)
        rc = pg.reject(types.SimpleNamespace(gate="strategy"))
        assert rc == 0
        block = gate_block(state.read_text(encoding="utf-8"), "strategy")
        assert 'status: "rejected"' in block
    finally:
        restore_paths(backups)
        restore_state(state, log, metadata, sb, lb, mb)

def test_placeholder_idea_blocks_p2():
    # The shipped placeholder idea-brief must not satisfy the real-idea guard.
    result = run(".pipeline/scripts/pipeline.py", "run", "P2")
    assert result.returncode == 3
    assert "BLOCKED" in result.stdout

def test_stage_complete_p1_blocks_until_real_idea(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        result = run(".pipeline/scripts/pipeline.py", "stage", "complete", "P1")
        assert result.returncode == 0
        assert "  P2: blocked_until_real_idea" in state.read_text(encoding="utf-8")
    finally:
        restore_state(state, log, metadata, sb, lb, mb)

def test_mode_set_updates_state(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        result = run(".pipeline/scripts/pipeline.py", "mode", "set", "high-assurance")
        assert result.returncode == 0
        assert 'mode: "high-assurance"' in state.read_text(encoding="utf-8")
    finally:
        restore_state(state, log, metadata, sb, lb, mb)

def test_reopen_resets_downstream_phases_gates_and_logs_reason(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    backups = backup_paths(tmp_path, "docs/20-product/prd.md", "docs/20-product/pm-critic-report.md")
    try:
        write_real_product_artifacts()
        assert run(".pipeline/scripts/pipeline.py", "stage", "complete", "P5").returncode == 0
        assert run(".pipeline/scripts/pipeline.py", "gate", "request", "product").returncode == 0
        result = run(".pipeline/scripts/pipeline.py", "reopen", "P5", "--reason", "technical infeasibility found in P7")
        assert result.returncode == 0
        text = state.read_text(encoding="utf-8")
        assert "  P5: ready" in text
        for phase in ("P6", "P7", "P8", "P9"):
            assert f"  {phase}: waiting" in text
        for gate in ("product", "architecture", "release"):
            assert 'status: "not_requested"' in gate_block(text, gate)
        assert "technical infeasibility found in P7" in log.read_text(encoding="utf-8")
        data = json.loads(metadata.read_text(encoding="utf-8"))
        assert data["reopens"][-1]["phase"] == "P5"
    finally:
        restore_paths(backups)
        restore_state(state, log, metadata, sb, lb, mb)

def test_reopen_requires_reason_and_preserves_state(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        before = state.read_text(encoding="utf-8")
        result = run(".pipeline/scripts/pipeline.py", "reopen", "P5")
        assert result.returncode != 0
        assert state.read_text(encoding="utf-8") == before
    finally:
        restore_state(state, log, metadata, sb, lb, mb)

def test_status_warns_when_completed_artifact_is_stale(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    backups = backup_paths(tmp_path, "docs/00-idea/idea-brief.md")
    try:
        write_file("docs/00-idea/idea-brief.md", "# Idea\n\nThis is a real idea body long enough to satisfy the guard for the phase completion hash test.\n")
        assert run(".pipeline/scripts/pipeline.py", "stage", "complete", "P1").returncode == 0
        write_file("docs/00-idea/idea-brief.md", "# Idea\n\nThis changed after completion and should trigger a stale artifact warning.\n")
        result = run(".pipeline/scripts/pipeline.py", "status")
        assert result.returncode == 0
        assert "Stale artifact warnings:" in result.stdout
        assert "docs/00-idea/idea-brief.md is changed" in result.stdout
    finally:
        restore_paths(backups)
        restore_state(state, log, metadata, sb, lb, mb)

def test_product_gate_requires_real_prd_and_critic_report(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        result = run(".pipeline/scripts/pipeline.py", "gate", "request", "product")
        assert result.returncode == 3
        assert "docs/20-product/prd.md" in result.stdout
        assert "docs/20-product/pm-critic-report.md" in result.stdout
    finally:
        restore_state(state, log, metadata, sb, lb, mb)

def test_strategy_gate_requires_red_team_in_standard_mode(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    backups = backup_paths(tmp_path, "docs/10-strategy/decision-memo.md", ".pipeline/reports/strategy-red-team.md")
    try:
        write_file("docs/10-strategy/decision-memo.md", "# Decision Memo\n\nReal decision memo.\n")
        result = run(".pipeline/scripts/pipeline.py", "gate", "request", "strategy")
        assert result.returncode == 3
        assert "strategy-red-team.md" in result.stdout
    finally:
        restore_paths(backups)
        restore_state(state, log, metadata, sb, lb, mb)

def test_gate_request_refused_until_phase_complete_keeps_state_valid(tmp_path):
    # Requesting a gate before its phase is complete must be refused rather than
    # producing a state that validate_state.py rejects. architecture has no
    # artifact preconditions, so it isolates the phase-completion guard.
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        result = run(".pipeline/scripts/pipeline.py", "gate", "request", "architecture")
        assert result.returncode == 3
        assert "P6 must be complete" in result.stdout
        assert 'status: "not_requested"' in gate_block(state.read_text(encoding="utf-8"), "architecture")
        valid = run(".pipeline/scripts/validate_state.py")
        assert valid.returncode == 0, valid.stdout
    finally:
        restore_state(state, log, metadata, sb, lb, mb)

def test_validate_state_catches_gate_without_completed_phase(tmp_path):
    state, log, metadata, sb, lb, mb = backup_state(tmp_path)
    try:
        text = state.read_text(encoding="utf-8")
        text = text.replace('  product:\n    status: "not_requested"', '  product:\n    status: "awaiting_approval"', 1)
        state.write_text(text, encoding="utf-8")
        result = run(".pipeline/scripts/validate_state.py")
        assert result.returncode == 1
        assert "product gate is awaiting_approval but P5 is not complete" in result.stdout
    finally:
        restore_state(state, log, metadata, sb, lb, mb)
