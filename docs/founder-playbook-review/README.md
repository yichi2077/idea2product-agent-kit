# Founder's Playbook → idea2product-agent-kit: Review & Incremental Plan

A deep review of Anthropic's **[The Founder's Playbook](https://claude.com/blog/the-founders-playbook)** (2026-05-14) and the user-supplied article distilling its Idea-stage validation methodology, mapped against this kit, with a prioritized incremental development plan.

| Doc | Contents |
|---|---|
| [00-article-methodology.md](00-article-methodology.md) | Faithful extraction of the article's 6-step validation flow + central thesis |
| [01-pipeline-capability-map.md](01-pipeline-capability-map.md) | What the pipeline already does (engine wiring + article-step coverage matrix) |
| [02-source-research.md](02-source-research.md) | The full playbook (Idea→MVP→Launch→Scale); complementary points beyond the article |
| [03-gap-analysis-and-decisions.md](03-gap-analysis-and-decisions.md) | Prioritized gaps (G1–G12), adopt/decline decisions with rationale |
| [04-incremental-dev-plan.md](04-incremental-dev-plan.md) | Tier 1/2/3 increments with exact files, changes, acceptance criteria, sequencing |
| [05-implementation-log.md](05-implementation-log.md) | What shipped + verification (Tier 1, new P6 phase + renumber, Phase A/B) |
| [06-occam-dev-plan.md](06-occam-dev-plan.md) | Necessity×done quadrant plan: do-first / keep-harden / don't / keep-for-now |
| [07-playbook-fidelity-audit.md](07-playbook-fidelity-audit.md) | Final audit: does the kit embody the playbook's full methodology + spirit? (closed loop) |
| [08-ux-skills-invocation-audit.md](08-ux-skills-invocation-audit.md) | UX audit: every feature reachable in-chat via skill/NL, nothing forced to a terminal (2 fixes) |
| [09-e2e-validation-report.md](09-e2e-validation-report.md) | Sandbox P1→P10 dry-run (no code): all phases/gates pass; 1 bug found + fixed (bias-watch false positive) |
| [10-50-lens-audit-and-final-plan.md](10-50-lens-audit-and-final-plan.md) | Current 50-lens audit pass: article + official playbook + live repo, with final no-new-gate plan |

**Headline:** the kit already encoded ~70% of the methodology; we landed the rest under a first-principles / Occam filter. Idea + MVP methodology is now **fully embodied** — and **exceeded** on the playbook's central warning: *"confirmation bias now has a research engine"* is turned into a guardrail the `doctor`/`gate` enforce over evidence provenance. Headline structural change: a new **P6 Validation Prototype** phase (pipeline now P1–P10). Launch/Scale ops are a deliberate scope boundary. See [07](07-playbook-fidelity-audit.md).
