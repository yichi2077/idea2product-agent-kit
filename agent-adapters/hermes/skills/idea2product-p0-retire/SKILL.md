---
name: idea2product-p0-retire
description: "Retire or abandon the current idea-to-product project only after showing the current handoff, collecting explicit confirmation, and recording a non-empty reason."
---

# idea2product-P0-retire

Use this when the user wants to abandon, terminate, archive, or retire the current
idea-to-product project. Retire marks unfinished phases as `retired`; it does not
delete files, erase completed work, or skip a phase inside an active project.

Retirement is a state-changing operation. Never run it on a guess.

## Precheck

1. Walk upward from the current directory until `.pipeline/scripts/pipeline.py` exists.
2. If it does not exist, this workspace has no pipeline yet — tell the user to run
   `$idea2product-p0-guided-flow` to initialize it, then stop. Do not scaffold from
   this skill.
3. Run the read-only handoff brief first (use `python` on Windows):

```bash
python3 .pipeline/scripts/pipeline.py handoff
```

Summarize the current phase, completed phases, gates, and next action before asking
for confirmation.

## Mandatory dialogue — do NOT skip

Before running retire, ask the user and WAIT for both:

1. **Explicit confirmation** — the user must clearly say they want to retire this project.
2. **Reason** — the concrete reason for abandoning or archiving this pipeline.

Hard rules:

- If confirmation is missing, stop and ask for it.
- If the reason is missing or vague, ask again. Do not invent the reason.
- If the user is trying to redo earlier work, use `$idea2product-p0-rollback` instead.
- If the user only wants to check whether retirement is appropriate, run no state-changing
  command; explain the current status and options.

Then confirm back and wait for an explicit "yes":

> I'll retire this pipeline: unfinished phases will be marked `retired`, existing files
> stay in place, and future work requires reopening a completed phase if you want to
> resume. Reason: `<reason>`. Proceed?

## Execute

Only after explicit confirmation and a non-empty reason, run (use `python` on Windows):

```bash
python3 .pipeline/scripts/pipeline.py retire --reason "<reason from the user>"
```

If the engine rejects the request, relay the exact reason and stop. Never hand-edit
state files.

## Broadcast result

After a successful retire, run:

```bash
python3 .pipeline/scripts/pipeline.py status
```

Summarize:

- Which phases are now complete and which were marked retired.
- That files were not deleted.
- That the reason was recorded in `.pipeline/state/decision-log.md`.
- That resuming meaningful work requires `$idea2product-p0-rollback` / `reopen <completed phase>`.

## Never

- Never run `retire` without explicit confirmation and a user-provided reason.
- Never use retire to skip a blocked gate or bypass phase work.
- Never approve gates, edit state directly, or delete project files.
