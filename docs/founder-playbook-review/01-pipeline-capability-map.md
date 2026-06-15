# 01 — Pipeline Capability Map (vs the article's 6 validation steps)

> What the idea2product pipeline **already does**, mapped against the article methodology in [00](00-article-methodology.md).
> Key finding: the pipeline is **far more sophisticated than its README implies** — most of the article's methodology already exists in vendored skills. The real opportunities are about **placement, required-vs-optional status, and a few specific missing techniques**, not wholesale gaps.

## How the engine is wired (for planning increments)

- **Skills are thin entry points** (`skills/idea2product-p*/SKILL.md`, 40–138 lines). They mostly tell the agent to `pipeline.py run P<n>` and follow the printed recipe.
- **Recipes** (`pipeline-template/.pipeline/recipes/p*.yaml`) are the real orchestration: each declares `required_skills`, `conditional_skills`, `optional_skills`, `non_skill_process`, `required_context`, `outputs`, `completion_commands`. Skills are referenced as `$skill-name`.
- **Vendored skill library** (`pipeline-template/.pipeline/vendor/{strategy,product,engineering}/*/SKILL.md`) — 34 reusable skills (PM-Skills + strategy + engineering). This is where the methodology lives.
- **Templates** (`pipeline-template/.pipeline/templates/*.md`) — output scaffolds the agent fills.
- **State registers** (`pipeline-template/.pipeline/state/`): `assumption-register.yaml`, `risk-register.yaml`, `decision-log.md`, `pipeline-state.yaml` — persistent cross-phase evidence/assumption tracking.
- **Gates**: `pipeline_gate.py` records human approval (light/strict mode) at Strategy (P3), Product (P5), Architecture (P6), Release (P8).
- **Engine**: `pipeline.py` (39KB) runs phases, validates deliverables, auto-commits. `doctor` checks state consistency.
- **Four-copy sync**: editing a skill means editing the canonical copy then running `scripts/sync_bundled_copies.py --write` (see project memory [[four-copy-sync]]). Bundled mirrors live under `agent-adapters/hermes` & `agent-adapters/openclaw` and `skills/`.

## Coverage matrix — article step → pipeline reality

| Article step | Where in pipeline | Status | Notes |
|---|---|---|---|
| **1. Idea → falsifiable hypothesis** (who/frequency/severity/workaround/loss) | P1 `idea-brief.md`; P4 `$define-hypothesis`, `$define-problem-statement` | **Partial / late** | idea-brief captures target user, problem, urgency, cost-of-doing-nothing, stop conditions — but NOT framed as one falsifiable hypothesis with **frequency** + **quantified severity** + **current workaround**. The rigorous `$define-hypothesis` (falsifiable, success metric, validation approach) lives in **P4**, after all strategy work. |
| **2. AI as devil's advocate at EVERY stage** ("confirmation bias has a research engine") | `$assumption-challenger` (req P1, opt P2/P3/P9); `red-team-strategy.md` (P3); `red-team-architecture.md` (P6); `$utility-pm-critic` (P5) | **Strong but uneven** | Genuinely good red-team infra. BUT adversary is **required only at P1**; optional/absent at P2/P4/P9. No **confirm-vs-challenge asymmetry** guard. No evidence-provenance tracking (was an assumption validated by users, or just by AI desk research?). |
| **3. Competitive landscape** (4 layers; competitor-review mining; steelman rival) | P2 `existing-solutions-scan.md` + `$market-research` | **Partial** | existing-solutions-scan is excellent (direct/indirect/substitutes/OSS/SaaS → use/buy/partner/build/retire decision — a real "should you build at all" forcing function). `$market-research` adds rigorous TAM/SAM/SOM triangulation + survey/segmentation. **Missing the article's specific techniques**: explicit "potential acquirers / adjacent movers" layers, **competitor-review mining** (top-5 recurring pains from G2/Reddit/App Store as free qual research), and **steelman-the-rival** ("why they win, you fail"). |
| **4. Customer-discovery interviews** (who+where, past-behavior questions, bias audit, per-interview debrief, 5-interview cadence, asymmetry) | `$discover-interview-synthesis` (P4, **conditional**); `$assumption-challenger` mentions "problem interviews focused on current behavior" | **Weakest area** | The pipeline can run P1→P9 producing beautiful docs with **zero real user conversations**. Interview *synthesis* exists but is conditional ("only when raw interview material exists") and synthesis-only. **No skill/template for**: defining who to interview + where they congregate, drafting+auditing questions for leading/socially-desirable bias, past-behavior framing, per-interview debrief, the every-5 cadence, or the confirm/challenge asymmetry check. This is the article's most detailed step and the pipeline's thinnest. |
| **5. Stress-test solution design** (3 load-bearing assumptions + cheapest refutation; "solving validated problem or original?") | `red-team-strategy.md` ("load-bearing assumptions ranked by cheapest test + kill criterion"); `$assumption-challenger` (D/V/F/U mapping, risk×certainty); `$develop-solution-brief` (P4) | **Strong** | `red-team-strategy.md` literally implements "rank assumptions by cheapest test + kill criterion." `$assumption-challenger` adds the full Teresa-Torres OST + assumption mapping. **Missing**: the explicit "**are you now solving the problem validation revealed, or the one you walked in with?**" reframing check before committing to build. |
| **6. Smallest validation prototype** (ONE core interaction → 5 target users → go/no-go) | `$measure-experiment-design` (P4, **conditional**); `$assumption-challenger` (concept/usability/fake-door/concierge tests) | **Partial / heavyweight** | `$measure-experiment-design` is a rigorous **A/B test** design (variants, MDE, sample size, duration) — assumes traffic, too heavy for pre-build idea validation. The article's lightweight "one interaction, 5 users, observe behavior" maps better to `$assumption-challenger`'s concierge/fake-door tests, but there is **no required pre-build validation step or "build the single core interaction" gate** between P5 (PRD) and P8 (full build). measure-experiment-*results* runs at P9 (post-launch). |

## Infrastructure the article doesn't even mention (pipeline strengths to preserve)

- **Persistent assumption + risk registers** carried across all 9 phases — better than the article's per-interview debrief alone.
- **Existing-solutions-scan with a forced build/buy/partner/retire User Decision** that *blocks P2 completion while pending* — a structural "don't build what you should just buy" guard the article only implies.
- **Four human gates** + light/strict approval modes.
- **`$utility-pm-critic` run in a fresh context** against the finished PRD — a built-in fresh-eyes red-team.
- **`doctor` health check** for state/deliverable consistency.
- **Engineering rigor downstream** (TDD, systematic-debugging, verification-before-completion, code-review skills) for P7/P8.

## One-line synthesis

The pipeline already encodes ~70% of the article's methodology, but its disconfirmation discipline is **optional where the article says it must be mandatory**, and its weakest seam is exactly the article's strongest claim: **real customer conversations as required, first-class evidence** — and the **lightweight pre-build validation prototype**.
