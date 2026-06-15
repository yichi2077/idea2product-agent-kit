# pipeline-gate

Prepare a gate decision for a human and record their verdict. Gates are the only human-owned
checkpoints in the pipeline. This skill must never let the agent approve a gate on its own.

## Rules

- Implicit invocation is disabled. Use only when a recipe lists `$pipeline-gate`.
- Record outputs in the configured pipeline files.

## At a gate

1. Make sure the gated phase is complete, then request the gate:
   `python3 .pipeline/scripts/pipeline.py gate request <strategy|product|architecture|release> --confidence <high|medium|low> --rationale "<grounded in open assumptions/risks>"`
2. **STOP and hand off to the human.** Present, in the conversation:
   - the decision artifact for this gate (decision-memo / PRD / ADRs),
   - your stated confidence and why,
   - the open assumptions and risks (`pipeline.py handoff`).
   Ask the human to approve or reject.
3. **Record the human's verdict — never decide yourself:**
   - **Light mode (default):** ONLY after the human explicitly approves in the conversation, run
     `python3 .pipeline/scripts/pipeline_gate.py approve <gate> --rationale "<the human's own reason>"`.
     To reject: `... reject <gate> --rationale "<their reason>"`. Use their words, not yours.
   - **Strict mode:** you cannot approve. Tell the human to run
     `python3 .pipeline/scripts/pipeline_gate.py approve <gate>` in a SEPARATE real OS terminal and
     type the challenge code printed at request time.

   Check the active mode with `python3 .pipeline/scripts/pipeline.py gate mode` if unsure.

## Never

- Never run `approve` / `reject` without an explicit human decision in the current conversation.
- Never invent, guess, or supply your own rationale for the human.
- Never edit gate fields in `pipeline-state.yaml` directly.
