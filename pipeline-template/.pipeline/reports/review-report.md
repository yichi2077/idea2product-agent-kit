# Review Report

Generated: 2026-06-12

## Findings

1. The previous implementation exposed one global orchestrator skill but did not expose P1-P9 as individually callable Codex skills.
2. Status and resume existed only as low-level command concepts; resume was missing from the CLI.
3. `pipeline gate request <gate>` updated the first `requested_at` and `challenge` fields in the state file instead of the target gate block.
4. `pipeline_gate.py approve <gate>` could approve the first awaiting gate instead of the requested gate block.
5. The package was not separated into a GitHub-ready user-facing folder.

## Fixes

1. Added user-level explicit Codex skills:
   - `idea2product-p1-idea-expansion`
   - `idea2product-p2-strategy-analysis`
   - `idea2product-p3-strategy-decision`
   - `idea2product-p4-product-discovery`
   - `idea2product-p5-product-definition`
   - `idea2product-p6-architecture-handoff`
   - `idea2product-p7-feature-specification`
   - `idea2product-p8-build-release`
   - `idea2product-p9-outcome-review`
2. Added `idea2product-p0-status` and `idea2product-p0-resume` user-level skills.
3. Kept and updated `idea2product-p0-guided-flow` as the guided end-to-end orchestrator.
4. Added `python .pipeline/scripts/pipeline.py resume`.
5. Scoped gate request and gate approval updates to the target gate block.
6. Replaced placeholder `link_skills.py` with an idempotent active-skill mapping script.
7. Added multi-agent adapters so the pipeline is not Codex-only:
   - Cursor project rule
   - Claude Code `CLAUDE.md`
   - OpenCode project agent
   - Hermes context and skills
   - OpenClaw bootstrap files and skills
   - Generic `AGENTS.md`
8. Added a shared agent operating guide under `agent-adapters/common/`.
9. Fixed cross-project startup: `idea2product-p0-guided-flow` now bundles a pipeline template, automatically initializes a workspace that lacks `.pipeline/scripts/pipeline.py`, and then continues the requested status/resume/P1-P9 command.
10. Made initialization non-destructive by default for existing projects: directories are merged, existing files are preserved, and an existing `AGENTS.md` gets a sidecar `AGENTS.idea2product.md`.
11. Fixed malformed P2/P3/P4/P5/P6/P8 recipe YAML and renamed the P6 recipe to `p6-architecture-handoff.yaml` for phase naming consistency.
12. Added recipe schema and active-skill validation through `.pipeline/scripts/validate_recipes.py`, now run by both verification scripts and pytest.
13. Expanded recipes to match the plan more closely:
   - P3/P5/P6/P8 include `$pipeline-gate`.
   - P4 includes `$define-prioritization-framework` and `$develop-solution-brief`.
   - P7 records the required Spec Kit command chain as `external_tools`.
   - P9 includes `$iterate-pivot-decision`.
14. Added `docs/PIPELINE-SKILL-MAP.md` documenting every P1-P9 entry skill, its underlying recipe skills, and each source family.
15. Refined recipes to separate `required_skills`, `conditional_skills`, and `optional_skills` instead of treating every phase capability as mandatory.
16. Removed `$pipeline-gate` from P3/P5/P6/P8 recipe skill lists; gates are now represented as non-skill pipeline commands.
17. Made P7 consume approved Specify Packets by default and call `$prd-to-speckit-handoff` only when packets are missing, stale, re-approved, or fail traceability.
18. Moved P2 `$financial-analyst`, P6 `$develop-spike-summary`, and P8 `$systematic-debugging` to conditional skills with explicit evidence/failure conditions.
19. Added Product on Purpose skills `$discover-interview-synthesis` and `$iterate-lessons-log` to the vendored and active skill set.
20. Added `pipeline stage complete <phase>` so phase recipes can complete stage state without using gate/orchestrator skills recursively.
21. Fixed Windows junction cleanup in `link_skills.py` so active skill relinking works reliably.

## Remaining Constraints

- Gate approval still requires a human interactive terminal.
- First real P1-P3 validation remains pending until the user supplies a real idea.
- `gh` CLI remains unavailable on this machine.
- Adapter installers copy host-specific instruction files but do not configure model providers or account credentials for those hosts.
- P7 still depends on a project environment that provides the external Spec Kit commands; those commands are validated as recipe requirements but are not bundled as prompt skills.
- Conditional skills are validated for existence, but their run conditions still require agent judgment and real evidence.
