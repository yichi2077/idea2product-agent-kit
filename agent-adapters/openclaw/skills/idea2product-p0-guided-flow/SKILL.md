---
name: idea2product-p0-guided-flow
description: "Guide a user through the full idea-to-product pipeline from initial idea through strategy, product, architecture, delivery, and outcome review; choose the next step from state, invoke the matching P1-P9 skill, request gates when needed, and keep the user oriented."
---

# idea2product-P0-guided-flow

Use this as the top-level guided entrypoint for the local `.pipeline` system in the current repository. It is the one-call assistant that keeps the user moving through the next correct step.

## Interaction model

The user drives this kit by talking to you and invoking skills — not by typing pipeline commands. You run `pipeline.py` on their behalf via the shell and report back in plain language. `pipeline.py` is the deterministic engine you operate; it is not the user's interface. The single exception is gate approval: the user runs `pipeline_gate.py approve` themselves in a real terminal, because a human (not the agent) must be the approval anchor.

## First Checks

1. Walk upward from the current directory until `.pipeline/scripts/pipeline.py` exists.
2. If `.pipeline` already exists, drive everything through the repo-local script:

```bash
python3 .pipeline/scripts/pipeline.py status
python3 .pipeline/scripts/pipeline.py resume
```

3. If `.pipeline` does NOT exist, initialize this workspace once using the entry
   script bundled with this skill, then use the repo-local script from then on.
   Use the path that matches where this skill is installed:

```bash
# Claude Code (personal skills)
python3 "$HOME/.claude/skills/idea2product-p0-guided-flow/scripts/pipeline_entry.py" init .

# Codex / AgentSkills
python3 "$HOME/.agents/skills/idea2product-p0-guided-flow/scripts/pipeline_entry.py" init .
```

   Add `--force` only when the user explicitly wants to overwrite an existing scaffold.
   Initialization does not run the test suite; it only creates `.pipeline`, `docs`,
   and the host wiring, and links the vendored skills.
   The bare guided-flow command only auto-initializes empty directories or `.git`-only
   empty repos. In a non-empty directory, run `init .` explicitly or pass `--auto-init`
   after confirming this is the intended target.

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

1. Run `python3 .pipeline/scripts/pipeline.py handoff` (use `python` on Windows). It is read-only and consolidates current phase, next step, gate states, recorded decisions, open assumptions/risks, and any stale outputs. Summarize it for the user — this is how you and the user re-orient at the start of any session.
2. If a ready phase is shown, use the corresponding numbered `idea2product-Px-*` skill.
3. If a real idea is missing, ask the user for the real idea instead of inventing one.
4. If a gate is awaiting approval, prepare the decision context and tell the user the manual approval command.
5. If the handoff reports a **stale** output (a completed phase's file changed after completion), confirm with the user whether the change is harmless or whether the affected phase must be reworked.

## Rework

When downstream work proves an upstream phase is wrong or stale, reopen it — never hand-edit state files:

```bash
python3 .pipeline/scripts/pipeline.py reopen P5 --reason "technical infeasibility found in P7"
```

Reopen rolls the target and downstream phases back, clears affected gates, and logs the reason. Only a completed phase can be reopened.

## Gate Rules

Agents may request gates but must not approve gates. When you request a gate, state your confidence in the decision context you prepared, grounded in the open assumptions and risks:

```bash
python3 .pipeline/scripts/pipeline.py gate request strategy --confidence high|medium|low --rationale "what drives that confidence"
```

The user sees that confidence when they approve, so they can vary their scrutiny. Approval is done by the user in a real interactive terminal:

```powershell
python .pipeline/scripts/pipeline_gate.py approve strategy
```

Do not bypass with `--yes`, `--force`, CI, pipes, redirects, environment variables, or direct state edits.

## Verification

After updating state, confirm the workspace is consistent:

```bash
python3 .pipeline/scripts/pipeline.py status
```

`.pipeline/scripts/verify.sh` on macOS/Linux and `.pipeline/scripts/verify.ps1`
on Windows run the full developer test suite (requires `pytest` and `pyyaml`);
use them for maintaining the kit, not for everyday runs.
