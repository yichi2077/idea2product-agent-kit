---
name: idea2product-p0-rollback
description: "Roll the idea-to-product pipeline back to an earlier completed phase using the reopen command — only after confirming the target phase, the affected reports, and the reason with the user; never reopen without explicit confirmation."
---

# idea2product-P0-rollback

Use this when the user wants to undo pipeline progress — a strategy pivot, a product
rebuild, or any case where downstream work proved an upstream phase wrong or stale. You
operate `pipeline.py reopen` on the user's behalf; the user talks, you run the command.

Reopen is **destructive**: it rolls the target phase back to `ready`, resets every
downstream phase to `waiting`, and clears the approved gates in that range. So a rollback
must never fire on a guess. Collect explicit confirmation first, every time.

## Precheck

1. Walk upward from the current directory until `.pipeline/scripts/pipeline.py` exists.
   If it does not, this workspace has no pipeline yet — tell the user to run
   `$idea2product-p0-guided-flow` to initialize it, then stop.
2. Run the read-only handoff to see the current phases and which are `complete`
   (use `python` on Windows):

```bash
python3 .pipeline/scripts/pipeline.py handoff
```

Only a phase whose status is `complete` can be reopened. Note which phases qualify before
you ask anything.

## Mandatory dialogue — do NOT skip

Before running anything, ask the user and WAIT for answers to all three. Never infer or
invent these:

1. **目标阶段 / Target phase** — exactly which completed phase to roll back to (P1–P10)?
2. **涉及报告 / Affected reports** — which rejected or to-be-rewritten documents/reports
   triggered this rollback?
3. **回退理由 / Reason** — the concrete fact, strategic change, or rework cause behind it?

Hard rules:

- If the user has not explicitly named a target phase, you MUST ask — do not pick one.
- If any of the three answers is missing or vague, ask again. Do not proceed on partial input.
- The target phase must currently be `complete`. If it is not, relay the engine's reason
  and stop — do not try to force it.

Then confirm back and wait for an explicit "yes":

> I'll reopen `<Phase>`: it returns to `ready`, all downstream phases become `waiting`,
> and these gates are cleared and will need re-approval later: `<gates>`. Proceed?

Compute `<gates>` from the phase→gate map — a gate is cleared when its phase is at or after
the target:

| Gate | Phase |
|------|-------|
| strategy | P3 |
| product | P5 |
| architecture | P7 |
| release | P9 |

(e.g. reopening P5 clears product, architecture, and release; strategy stays because P3 < P5.)

## Execute

Only after an explicit yes, assemble a detailed reason (the affected reports plus the cause)
and run (use `python` on Windows):

```bash
python3 .pipeline/scripts/pipeline.py reopen <Phase> --reason "<affected reports> — <reason>"
```

- `--reason` is required and must be non-empty; the engine rejects an empty reason.
- If the engine prints `Cannot reopen <Phase>: only a completed phase can be reopened`,
  relay that to the user and stop. Never bypass it, never hand-edit state files.

## Broadcast result

After a successful reopen, run `python3 .pipeline/scripts/pipeline.py status` and summarize
for the user in plain language:

- Which phase is now `ready`, and which downstream phases are now `waiting`.
- Which gates were invalidated (now `not_requested`) and must be re-approved later.
- If P1–P3 was reopened, that `pilot_validation` reverted to `PENDING_REAL_IDEA`.
- That the reason was recorded in `.pipeline/state/decision-log.md`.
- The next focus: rework the reopened phase via its `idea2product-Px-*` skill, then
  re-request the affected gates when the new work is ready.

## Never

- Never run `reopen` without the user's explicit target phase and confirmation.
- Never invent the reason or the affected reports — they come from the user.
- Never hand-edit state files; never approve a gate without the user's explicit decision (light mode records their in-chat approval; strict mode is terminal-only).
