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

3. If `.pipeline` does NOT exist, or the user asks "what is this" / "how do I start",
   run the first-run onboarding before initialization or routing. Do not scaffold until
   the user has answered "what's your idea?"
4. After onboarding captures the idea, initialize this workspace once using the entry
   script bundled with this skill, then use the repo-local script from then on.
   Use the path that matches where this skill is installed:

```bash
# Claude Code (personal skills)
python3 "$HOME/.claude/skills/idea2product-p0-guided-flow/scripts/pipeline_entry.py" init .

# Codex / AgentSkills
python3 "$HOME/.agents/skills/idea2product-p0-guided-flow/scripts/pipeline_entry.py" init .

# Hermes
python3 "$HOME/.hermes/skills/idea2product-p0-guided-flow/scripts/pipeline_entry.py" init .
```

   Add `--force` only when the user explicitly wants to overwrite an existing scaffold.
   Initialization does not run the test suite; it only creates `.pipeline`, `docs`,
   and the host wiring, and links the vendored skills.
   The bare guided-flow command only auto-initializes empty directories or `.git`-only
   empty repos. In a non-empty directory, run `init .` explicitly or pass `--auto-init`
   after confirming this is the intended target.
   This low-level auto-init behavior is for direct CLI/tool use only; when operating as
   this skill, always complete the onboarding dialogue first.

## First-run onboarding

When `.pipeline` is absent, or the user asks what the kit is or how to start, orient before running any init command:

1. Explain that idea2product turns a raw idea into a shipped product for a solo operator. The user talks; you run the engine commands. The only normal command the user runs directly is gate approval, because a human must be the approval anchor.
2. Walk the path in one line each: P1 idea, P2 strategy analysis, P3 strategy decision `[Strategy Gate]`, P4 product discovery, P5 PRD `[Product Gate]`, P6 architecture/ADR `[Architecture Gate]`, P7 feature spec, P8 build/release `[Release Gate]`, P9 outcome review.
3. Mention continuation and operations: status, resume, rollback, doctor health check, and retire.
4. Ask exactly: "What's your idea?" Wait for the user's answer. Only then scaffold/init and start P1 from that idea.
5. Do not run the entry script before the answer, even if the target directory is empty and the entry script would auto-initialize safely.

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
- `$idea2product-p0-rollback`: roll a completed phase (and its downstream) back.
- `$idea2product-p0-doctor`: run the read-only workspace health check.
- `$idea2product-p0-retire`: retire the project after explicit confirmation and a reason.

## Guided Flow

1. Run `python3 .pipeline/scripts/pipeline.py handoff` (use `python` on Windows). It is read-only and consolidates current phase, next step, gate states, recorded decisions, open assumptions/risks, and any stale outputs. Summarize it for the user — this is how you and the user re-orient at the start of any session.
2. If a ready phase is shown, use the corresponding numbered `idea2product-Px-*` skill.
3. If a real idea is missing, ask the user for the real idea instead of inventing one.
4. If a gate is awaiting approval, prepare the decision context and tell the user the manual approval command.
5. If the handoff reports a **stale** output (a completed phase's file changed after completion), confirm with the user whether the change is harmless or whether the affected phase must be reworked.
6. Do not run `stage complete Px` until that phase is the current `ready` phase and its recipe outputs exist and no longer contain scaffold placeholders. The engine rejects skipped phases and placeholder outputs.

## Your options now

After each handoff or resume summary, present a short state-aware menu in prose. Include only actions that are valid from the current state:

- Continue to the ready phase.
- Check status.
- Roll back a completed phase.
- Review overdue assumptions and risks.
- Run a health check via `$idea2product-p0-doctor`.
- Retire the project via `$idea2product-p0-retire`.

## Rework

When downstream work proves an upstream phase is wrong or stale, reopen it — never hand-edit state files:

```bash
python3 .pipeline/scripts/pipeline.py reopen P5 --reason "technical infeasibility found in P7"
```

Reopen rolls the target and downstream phases back, clears affected gates, and logs the reason. Only a completed phase can be reopened.

For a guided, confirmation-checked rollback, invoke `$idea2product-p0-rollback` instead of running `reopen` by hand — it collects the target phase, affected reports, and reason from the user before reopening.

For a direct health check, invoke `$idea2product-p0-doctor` instead of only describing
the `doctor` command. It runs the read-only check and summarizes missing, stale,
scaffold, or inconsistent state without changing files.

## Retiring a project

Retire means abandon/terminate the project pre-release; it is not a phase skip. Prefer
invoking `$idea2product-p0-retire` so the confirmation and reason capture are handled
consistently. Before running retire from this guided flow:

1. Summarize the current phase and any completed phases from `pipeline.py handoff`.
2. Ask the user to explicitly confirm retirement and provide the reason.
3. If confirmation or reason is missing, stop and ask for it.
4. Run:

```bash
python3 .pipeline/scripts/pipeline.py retire --reason "reason from the user"
```

5. Report that unfinished phases were marked retired and that resuming requires `reopen <completed phase>`.

## Gate Rules

Agents may request gates but must not approve gates. When you request a gate, state your confidence in the decision context you prepared, grounded in the open assumptions and risks:

Before requesting any gate, run:

```bash
python3 .pipeline/scripts/pipeline.py assumptions due
```

Surface any overdue assumptions or risks to the user and account for them in the confidence rationale.

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
