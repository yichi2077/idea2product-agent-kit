# Skills-First Interaction Plan

Date: 2026-06-13
Status: in progress
Trigger: re-review the kit on the premise that the user-facing interaction should be skills-based, not command-line.

## Judgment (research-grounded, independent)

Anthropic's own Agent Skills guidance endorses exactly the kit's architecture:
"scripts for deterministic tasks, natural language for judgment calls";
"Claude runs scripts via bash and receives only the output"; and **"the skill
wrapper is what gives the script context-awareness and a natural language
interface."** Skills in 2026 are *model-invoked* (Claude auto-discovers by
description); slash commands are the user-invoked surface.

Conclusion: the deterministic `pipeline.py` engine is correct and stays. The
fix is not removing the CLI — it is making **skills the complete primary
interface** and stopping the docs from teaching users to operate the CLI by
hand. The one deliberate exception is human gate approval
(`pipeline_gate.py approve/reject`), which must stay an out-of-agent terminal
command by security design — the human, not the model, is the trust anchor.

## Gaps found

- **G1 — stale orchestrator/continuation skills.** `idea2product-p0-guided-flow`,
  `-p0-status`, `-p0-resume` predate this cycle's features. None mention the
  handoff brief, `reopen` rework loop, the gate confidence signal, or staleness
  warnings. So the skills-first path cannot drive the full current workflow; a
  user who needs to rework or resume falls back to raw CLI.
- **G2 — CLI-first framing in docs.** `README.md` "Quick start" and
  `PIPELINE-USER-GUIDE.md` "Daily Commands" present raw `python3 pipeline.py …`
  as the user's daily interface, teaching the wrong mental model. The CLI is
  what the *agent* runs; the human runs only the gate-approval command.

## Changes (skills + docs only — no pipeline logic changes)

1. `idea2product-p0-guided-flow/SKILL.md`: state the interaction contract
   (user speaks naturally / invokes skills; agent drives `pipeline.py`; the only
   human-typed command is gate approval). Add resume→handoff, the `reopen`
   rework rule (never hand-edit state), staleness handling, and `--confidence`
   on gate requests. Keep it token-tight; point to the user guide for detail.
2. `idea2product-p0-resume/SKILL.md`: run `handoff` for the consolidated brief
   (decisions, open assumptions/risks, staleness) before continuing.
3. `idea2product-p0-status/SKILL.md`: note status surfaces staleness; point to
   `handoff` for the full brief.
4. `README.md`: reframe "Quick start" to skills-first — talk to the agent; it
   runs the pipeline. Keep the human gate-approval command prominent; demote
   other raw CLI to "what the agent runs under the hood / advanced."
5. `PIPELINE-USER-GUIDE.md`: reframe "Daily Commands" as agent-run on skill
   invocation; the user may run the read-only ones (status/handoff) to orient;
   gate approval stays the human command.

Out of scope: removing or hiding `pipeline.py`; adding new entry skills for
reopen/handoff (they are agent-internal moves the orchestrator drives, not
named user entry points); any change to phase skills P1–P9 (already correctly
agent-facing wrappers).

## Authoring discipline

Skill edits follow the kit's vendored `superpowers:writing-skills` guidance:
description = triggering conditions only (no workflow summary), token-efficient
bodies, progressive disclosure, cross-reference by name. Verification is via the
kit's own suite (`verify.sh`, `sync_bundles.py --check`) plus a re-read
confirming an agent following each skill would invoke handoff/reopen/confidence
at the right moments. (No subagent pressure tests — the harness reserves agent
spawning for explicit user request; the baseline gap here is established by
direct inspection.)
