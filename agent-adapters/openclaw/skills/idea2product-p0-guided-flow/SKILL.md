---
name: idea2product-p0-guided-flow
description: "Guide a user through the full idea-to-product pipeline from initial idea through strategy, product, architecture, delivery, and outcome review; choose the next step from state, invoke the matching P1-P9 skill, request gates when needed, and keep the user oriented."
---

# idea2product-P0-guided-flow

Use this as the top-level guided entrypoint for the local `.pipeline` system in the current repository. It is the one-call assistant that keeps the user moving through the next correct step.

## First Checks

1. Walk upward from the current directory until `.pipeline/scripts/pipeline.py` exists.
2. If `.pipeline` already exists, drive everything through the repo-local script:

```powershell
python .pipeline/scripts/pipeline.py status
python .pipeline/scripts/pipeline.py resume
```

3. If `.pipeline` does NOT exist, initialize this workspace once using the entry
   script bundled with this skill, then use the repo-local script from then on.
   Use the path that matches where this skill is installed:

```powershell
# Claude Code (personal skills)
python "$HOME/.claude/skills/idea2product-p0-guided-flow/scripts/pipeline_entry.py" init .

# Codex / AgentSkills
python "$HOME/.agents/skills/idea2product-p0-guided-flow/scripts/pipeline_entry.py" init .
```

   Add `--force` only when the user explicitly wants to overwrite an existing scaffold.
   Initialization does not run the test suite; it only creates `.pipeline`, `docs`,
   and the host wiring, and links the vendored skills.

## Explicit Skills

Phase skills:

- `$idea2product-p1-idea-expansion`: idea2product-P1-idea-expansion
- `$idea2product-p2-strategy-analysis`: idea2product-P2-strategy-analysis
- `$idea2product-p3-strategy-decision`: idea2product-P3-strategy-decision
- `$idea2product-p4-product-discovery`: idea2product-P4-product-discovery
- `$idea2product-p5-product-definition`: idea2product-P5-product-definition
- `$idea2product-p6-architecture-handoff`: idea2product-P6-architecture-handoff
- `$idea2product-p7-feature-specification`: idea2product-P7-feature-specification
- `$idea2product-p8-build-release`: idea2product-P8-build-release
- `$idea2product-p9-outcome-review`: idea2product-P9-outcome-review

Continuation skills:

- `$idea2product-p0-status`: report current state only.
- `$idea2product-p0-resume`: continue from current state.

## Guided Flow

1. Run `python .pipeline/scripts/pipeline.py resume`.
2. If resume prints a ready phase, use the corresponding numbered `idea2product-Px-*` skill.
3. If a real idea is missing, ask the user for the real idea instead of inventing one.
4. If a gate is awaiting approval, prepare the decision context and tell the user the manual approval command.

## Gate Rules

Agents may request gates but must not approve gates:

```powershell
python .pipeline/scripts/pipeline.py gate request strategy
```

Approval must be done by the user in a real interactive terminal:

```powershell
python .pipeline/scripts/pipeline_gate.py approve strategy
```

Do not bypass with `--yes`, `--force`, CI, pipes, redirects, environment variables, or direct state edits.

## Verification

After updating state, confirm the workspace is consistent:

```powershell
python .pipeline/scripts/pipeline.py status
```

`.pipeline/scripts/verify.ps1` runs the full developer test suite (requires
`pytest` and `pyyaml`); use it for maintaining the kit, not for everyday runs.
