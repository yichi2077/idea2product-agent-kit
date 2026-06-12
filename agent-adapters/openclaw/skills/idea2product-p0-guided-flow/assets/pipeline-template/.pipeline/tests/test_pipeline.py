import importlib.util
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
    state_bak = tmp_path / "state.yaml"
    log_bak = tmp_path / "log.md"
    shutil.copy2(state, state_bak)
    if log.exists():
        shutil.copy2(log, log_bak)
    return state, log, state_bak, log_bak

def restore_state(state, log, state_bak, log_bak):
    shutil.copy2(state_bak, state)
    if log_bak.exists():
        shutil.copy2(log_bak, log)

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

def test_gate_request_updates_target_gate_only(tmp_path):
    state, log, sb, lb = backup_state(tmp_path)
    try:
        result = run(".pipeline/scripts/pipeline.py", "gate", "request", "product")
        assert result.returncode == 0
        text = state.read_text(encoding="utf-8")
        strategy_block = text.split("  strategy:", 1)[1].split("  product:", 1)[0]
        product_block = text.split("  product:", 1)[1].split("  architecture:", 1)[0]
        assert 'status: "not_requested"' in strategy_block
        assert 'requested_at: null' in strategy_block
        assert 'status: "awaiting_approval"' in product_block
        assert 'requested_at: "' in product_block
    finally:
        restore_state(state, log, sb, lb)

def test_stage_complete_updates_phase_without_approving_gate(tmp_path):
    state, log, sb, lb = backup_state(tmp_path)
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
        restore_state(state, log, sb, lb)

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
    state, log, sb, lb = backup_state(tmp_path)
    try:
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
        restore_state(state, log, sb, lb)

def test_correct_challenge_approves(tmp_path):
    state, log, sb, lb = backup_state(tmp_path)
    try:
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
        block = gate_block(state.read_text(encoding="utf-8"), "strategy")
        assert 'status: "approved"' in block
    finally:
        restore_state(state, log, sb, lb)

def test_gate_reject_sets_rejected(tmp_path):
    state, log, sb, lb = backup_state(tmp_path)
    try:
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
        restore_state(state, log, sb, lb)

def test_placeholder_idea_blocks_p2():
    # The shipped placeholder idea-brief must not satisfy the real-idea guard.
    result = run(".pipeline/scripts/pipeline.py", "run", "P2")
    assert result.returncode == 3
    assert "BLOCKED" in result.stdout

def test_stage_complete_p1_blocks_until_real_idea(tmp_path):
    state, log, sb, lb = backup_state(tmp_path)
    try:
        result = run(".pipeline/scripts/pipeline.py", "stage", "complete", "P1")
        assert result.returncode == 0
        assert "  P2: blocked_until_real_idea" in state.read_text(encoding="utf-8")
    finally:
        restore_state(state, log, sb, lb)

def test_mode_set_updates_state(tmp_path):
    state, log, sb, lb = backup_state(tmp_path)
    try:
        result = run(".pipeline/scripts/pipeline.py", "mode", "set", "high-assurance")
        assert result.returncode == 0
        assert 'mode: "high-assurance"' in state.read_text(encoding="utf-8")
    finally:
        restore_state(state, log, sb, lb)
