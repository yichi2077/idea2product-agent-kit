# Changelog

All notable changes to `idea2product-agent-kit`.

## [Unreleased] — Founder's-Playbook validation increments

Brings Anthropic's *Founder's Playbook* validation methodology into the pipeline, applied under a first-principles / "如无必要勿增实体" filter. Full review, rationale, and decision log in [`docs/founder-playbook-review/`](docs/founder-playbook-review/).

### Added
- **P6 Validation Prototype phase** — the pipeline is now **10 phases**. Define the single core interaction, test a throwaway with ~5 target users, then decide go/pivot/waive. **Non-gated and waivable** with a recorded rationale (no hard floor). Phases renumbered: Architecture→**P7**, Feature-Spec→**P8**, Build→**P9**, Outcome→**P10**; Architecture Gate→P7, Release Gate→P9 (Strategy@P3, Product@P5 unchanged).
- **Confirmation-bias guardrail** — the assumption register gains provenance fields (`validation_method`, `user_contact_n`, `evidence_for`, `evidence_against`, `confidence`). `doctor` and `gate request` surface **non-blocking** warnings for assumptions closed without user contact, closed with zero disconfirming evidence, and register-wide supporting-vs-disconfirming asymmetry. (Turns "confirmation bias now has a research engine" into a guard only persistent state can run.)
- **Falsifiable-hypothesis** fields in the idea brief (persona / frequency / quantified loss / current workaround).
- **Competitor scan upgraded** — 4 layers (direct / indirect / potential acquirers / adjacent movers), review-mining (top complaints from App Store / G2 / Reddit), and steelman-the-rival.
- **PRD guardrails** — explicit Non-goals + evidence-gated feature-add bar ("real user signal, or founder enthusiasm?"); requirements must trace to the validated problem.
- **Customer-discovery interview-plan template** (who + where, bias-audited past-behavior questions, per-interview debrief, every-5 asymmetry guard) wired into P4 as a recommended step; reuses `$discover-interview-synthesis`.
- **PMF instruments** (Sean Ellis 40%, effort push-vs-pull, three R's) + false-PMF caution in outcome-review and the validation prototype.
- Required red-team (pre-mortem) checkpoint at P2 and P4; skeptic-check and moat-check prompts in decision/outcome templates.

### Fixed
- Confirmation-bias watch no longer false-positives on the seed bookkeeping assumption (A-0001), which the engine auto-closes at P1. Bookkeeping assumptions use `validation_method: n/a` and are exempt; real assumptions closed without user contact / without disconfirming evidence still fire. (Found by the end-to-end sandbox run — see `docs/founder-playbook-review/09-e2e-validation-report.md`.)

### Notes
- All additions are agent-agnostic and propagated to bundled copies via `scripts/sync_bundled_copies.py`.
- Deliberately **not** added (first-principles): a required pre-release security gate (off-thesis), a post-build architecture-memory nudge (redundant with ADRs). See [`docs/founder-playbook-review/06-occam-dev-plan.md`](docs/founder-playbook-review/06-occam-dev-plan.md).
