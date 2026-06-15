# 08 — UX / Skills-Invocation Audit

> Invariant audited: the kit is **skills-based** — the user's whole operation happens **inside the Agent chat**, via skill invocation or natural language. No new feature may force the user to a terminal, a manual file edit, or anything outside the conversation. (The agent runs the `pipeline.py` commands; the user talks.)
> Scope: the new Founder's-Playbook features **and** the project as a whole.

## How invocation works (so additions are judged against it)
- **Phases** are reached by entry skills `idea2product-pN-*` (or "run pN" / "next"); the agent runs `pipeline.py run PN` and follows the printed recipe **in chat**.
- **Skills install by glob** (`install.py` → `copy_skill_dirs` iterates `skills/`), and **scaffold copies all of `pipeline-template/`** (recipes + templates). So any new skill/recipe/template auto-propagates to every host install.
- **Templates** are filled **by the agent** during a phase and presented in chat; the user never hand-edits them.
- **Operations** (status, resume, rollback, doctor, retire, gates) each have a P0 skill; the agent runs the command and summarizes. Light gate mode (default) records approval **in chat**.

## New features — invocation verdict

| New feature | In-chat reach | Verdict |
|---|---|---|
| **P6 Validation Prototype** phase | Entry skill `idea2product-p6-validation-prototype` (glob-installed); listed in guided-flow walk + phase-skill list, PIPELINE-USER-GUIDE, common guide; "validation prototype" added to Cursor trigger keywords | **Reachable** via skill / "next" / NL |
| Interview-plan, validation-prototype, PMF, security-review, skeptic, pivot, non-goals | Recipe steps / templates the agent executes during the phase; surfaced when `run PN` prints the recipe | **In-chat** (agent-run, agent-filled) |
| Confirmation-bias watch (A1) | Prints in `doctor` (reached by `$idea2product-p0-doctor` / "run a health check" / "am I fooling myself?") **and** at every `gate request` (the in-chat decision point) | **Reachable** (after fix below) |
| Assumption provenance fields | Agent fills during P2/P4/P10; never a user edit | **In-chat** |

## Defects found & fixed (this audit)
1. **Cursor adapter stale phase ref** — `agent-adapters/cursor/.cursor/rules/idea2product.mdc` still said "P1-**P9** execution". The earlier renumber pass filtered to `.md/.yaml/.py` and **missed the `.mdc` extension**. → Fixed to "P1-P10" + added "validation prototype" to the rule's trigger keywords. A full **all-extensions** re-scan now reports zero stale phase refs anywhere.
2. **Bias-watch not advertised/relayed by the doctor skill** — `$idea2product-p0-doctor` ran the check (which now prints the watch) but its description/report guidance never mentioned it, so the flagship A1 feature wasn't discoverable by NL and the agent might gloss the non-blocking lines. → Description now triggers on "am I fooling myself / is my evidence solid"; the Report section now instructs the agent to **always relay** the Confirmation-bias watch lines.

## Whole-project posture (already strongly in-chat)
- Light gate mode is the **default** (approve in chat); the agent runs every `pipeline.py` command for the user.
- Onboarding is **zero-terminal** (`init` one-shot + agent auto-remediation), so even setup is in-chat where the host allows.
- All adapters (claude-code, cursor, codex, opencode, generic, hermes, openclaw) route through entry skills + the common guide + the `.pipeline` command surface — no host requires the user to operate the engine directly.

### Intentional, documented exceptions (not violations)
- **Strict gate mode** deliberately requires a human to enter a challenge code in a *separate* terminal — a security anchor, **opt-in**; the default light mode stays in chat.
- **Talking to ~5 real users** (P6) and **doing real interviews** (P4) are inherently outside the chat — that is the *methodology*, not a tooling gap. The agent does all the in-chat work around them: plan, bias-audited questions, debrief, synthesis, decision.

## Verdict
After the two fixes, **every new feature is reachable from inside the Agent chat via a skill or natural language**, with nothing pushed to a terminal or a manual file edit. The additions conform to the kit's skills-based UX model, and the project remains consistent end-to-end (`sync --check` clean, `doctor` healthy, zero stale phase references across all file types).
