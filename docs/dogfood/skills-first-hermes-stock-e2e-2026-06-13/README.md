# Skills-First Hermes E2E Dogfood: Historical Stock Backtest Idea

Date: 2026-06-13
Goal: Validate idea2product as a skills-first Hermes workflow, not as a product implementation.
Idea under test: A Hermes feature that accepts stock-selection standards and trading rules, goes back to each year from 2020 through 2026, chooses one continuous three-month window per year, runs historical-as-of selection/backtest logic, and returns trade blotters plus returns.

## Scope

This dogfood run tested whether a user can operate the current kit through the shipped `idea2product-*` skills:

- `idea2product-p0-guided-flow` via the Hermes skill install path.
- `idea2product-p0-status` and `idea2product-p0-resume`.
- `idea2product-p1-idea-expansion` through `idea2product-p9-outcome-review`.
- Human-only gate flow with simulated user approval through a pseudo-terminal.
- Product Gate stale-artifact refusal.

The run used deterministic synthetic market data. It did not attempt to build a production financial backtester or validate investment performance.

## Evidence

Baseline checks before fixes:

- `python3 scripts/sync_bundles.py --check`: passed.
- `python3 -m pytest pipeline-template/.pipeline/tests/test_pipeline.py`: 27 passed before changes.

First sandbox, engine-oriented:

- Evidence: local throwaway sandbox, not committed to the repository.
- Result: completed collection of evidence, but found a P0 blocker.
- Key finding: each gate approval recorded `approved`, but the guarded next phase stayed blocked:
  - Strategy approval left `P4: blocked_until_strategy_gate`.
  - Product approval left `P6: blocked_until_product_gate`.
  - Architecture approval left `P7: blocked_until_architecture_gate`.
  - Release approval left `P9: blocked_until_release_gate`.

Post-fix engine sandbox:

- Evidence: local throwaway sandbox, not committed to the repository.
- Result: P1-P9 and all four gates completed.
- Remaining finding: final handoff still showed seed assumption/risk records saying no real idea had been supplied.

Final skills-first Hermes sandbox:

- Evidence: local throwaway sandbox summary, not committed to the repository.
- Result: 0 findings.
- Flow used:
  - Installed Hermes adapter and user skills into isolated `HOME`.
  - Ran P0 using the Hermes skill path: `~/.hermes/skills/idea2product-p0-guided-flow/scripts/pipeline_entry.py init .`
  - Ran P0 status and resume/handoff.
  - Ran P1-P9 through each current phase skill protocol.
  - Simulated user approval for Strategy, Product, Architecture, and Release gates.
  - Verified non-TTY gate approval is still denied.
  - Verified stale PRD change is rejected by Product Gate.
  - Final handoff showed all gates approved and no stale no-real-idea assumption/risk.

## Bugs Found And Fixed

### P0: Gate approval did not unblock the next phase

Impact: A real user approving a gate would immediately stall. `p0-resume` could not find a ready next phase even though the gate was approved.

Fix:

- `pipeline_gate.py` now maps each gate to its guarded next phase and changes only the exact `blocked_until_<gate>_gate` state to `ready` after successful approval.
- Added regression coverage for all four gates.

### P2: Seed no-real-idea assumption/risk stayed open after P1

Impact: After a complete run, handoff still said no real idea had been supplied. That undermined trust in the state summary.

Fix:

- `stage complete P1` now closes the scaffold seed assumption `A-0001` and risk `R-0001` when `has_real_idea()` passes.
- Added regression coverage proving final handoff no longer surfaces those stale records.

### Skills UX: Hermes P0 init path was missing

Impact: The P0 guided-flow skill listed Claude and Codex install paths, but not Hermes. A Hermes user starting from skills could be sent to the wrong bootstrap command.

Fix:

- Added the Hermes path to `idea2product-p0-guided-flow/SKILL.md`.

### Skills UX: P1-P9 run commands were Windows-first

Impact: Phase skills showed a `powershell` block with `python ...`. On this macOS environment, `python` is not available, so following the skill literally would fail.

Fix:

- P1-P9 skills now show `python3 ...` for macOS/Linux and a separate `python ...` Windows command.

### Test harness: state tests polluted scaffold registers

Impact: After adding automatic register closure, tests that completed P1 with a real idea could leave scaffold registers closed and sync that bad state into embedded templates.

Fix:

- Test state backup/restore now also protects `assumption-register.yaml` and `risk-register.yaml`.

## Verification After Fixes

- `python3 -m pytest pipeline-template/.pipeline/tests/test_pipeline.py`: 29 passed.
- `python3 scripts/sync_bundles.py --check`: all mirrors in sync.
- Skills static check:
  - P0 guided-flow includes the Hermes init path.
  - P1-P9 include `python3` macOS/Linux commands and Windows alternatives.
  - All `agents/openai.yaml` policies keep `allow_implicit_invocation: false`.
- Final skills-first Hermes sandbox completed with 0 findings.

## Remaining Risks

- The final sandbox did not call a live Hermes LLM session. It validated installed Hermes-compatible skills and the exact skill protocols, but not model behavior quality.
- The test uses synthetic market data by design. Real data provider issues, corporate actions, survivorship bias, and market calendars remain product requirements for the stock-backtest idea, not kit workflow blockers.
- README states Python 3.10+, but the current local environment is Python 3.9.6 and all tested paths pass. The declared minimum may be stricter than the implementation currently needs.
