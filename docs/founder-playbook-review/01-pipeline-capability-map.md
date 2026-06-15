# 01 — Pipeline Capability Map (vs the article's 6 validation steps)

> What the idea2product pipeline **already does**, mapped against the article methodology in [00](00-article-methodology.md).
> Key finding: the pipeline is **far more sophisticated than its README implies** — most of the article's methodology already exists in vendored skills. The real opportunities are about **placement, required-vs-optional status, and a few specific missing techniques**, not wholesale gaps.
>
> Status note (2026-06-15): this map was first written before the Founder's-Playbook
> increment landed. It now reflects the current P1-P10 workflow: P6 is Validation
> Prototype, Architecture Gate is at P7, and Release Gate is at P9.

## How the engine is wired (for planning increments)

- **Skills are thin entry points** (`skills/idea2product-p*/SKILL.md`, 40–138 lines). They mostly tell the agent to `pipeline.py run P<n>` and follow the printed recipe.
- **Recipes** (`pipeline-template/.pipeline/recipes/p*.yaml`) are the real orchestration: each declares `required_skills`, `conditional_skills`, `optional_skills`, `non_skill_process`, `required_context`, `outputs`, `completion_commands`. Skills are referenced as `$skill-name`.
- **Vendored skill library** (`pipeline-template/.pipeline/vendor/{strategy,product,engineering}/*/SKILL.md`) — 34 reusable skills (PM-Skills + strategy + engineering). This is where the methodology lives.
- **Templates** (`pipeline-template/.pipeline/templates/*.md`) — output scaffolds the agent fills.
- **State registers** (`pipeline-template/.pipeline/state/`): `assumption-register.yaml`, `risk-register.yaml`, `decision-log.md`, `pipeline-state.yaml` — persistent cross-phase evidence/assumption tracking.
- **Gates**: `pipeline_gate.py` records human approval (light/strict mode) at Strategy (P3), Product (P5), Architecture (P7), Release (P9).
- **Engine**: `pipeline.py` runs P1-P10, validates deliverables, tracks phase hashes, requests gates, and surfaces `doctor` state consistency plus confirmation-bias warnings.
- **Four-copy sync**: editing a skill means editing the canonical copy then running `scripts/sync_bundled_copies.py --write` (see project memory [[four-copy-sync]]). Bundled mirrors live under `agent-adapters/hermes` & `agent-adapters/openclaw` and `skills/`.

## Coverage matrix — article step → pipeline reality

| Article step | Where in pipeline | Status | Notes |
|---|---|---|---|
| **1. Idea -> falsifiable hypothesis** (who/frequency/severity/workaround/loss) | P1 `idea-brief.md`; P4 `$define-hypothesis`, `$define-problem-statement` | **Landed** | P1 now asks for a single falsifiable hypothesis with persona, scenario, frequency, cause, quantified loss, and current workaround. P4 still deepens the product hypothesis after strategy approval. |
| **2. AI as devil's advocate at EVERY stage** ("confirmation bias has a research engine") | `$assumption-challenger` required in P1/P6 and required as a non-skill red-team process in P2/P4; `strategy-red-team.md` (P3); `$utility-pm-critic` (P5); `doctor` + gate request confirmation-bias watch over provenance fields | **Strong** | The weak spot from the first audit was closed: assumptions now carry `validation_method`, `user_contact_n`, `evidence_for`, and `evidence_against`; `doctor` warns on userless closes, zero disconfirming data, and register asymmetry. |
| **3. Competitive landscape** (4 layers; competitor-review mining; steelman rival) | P2 `existing-solutions-scan.md` + `$market-research` | **Landed** | P2 now requires direct, indirect/substitute, potential acquirer/incumbent, and adjacent-mover layers; competitor pain mining from reviews/forums; and a steelman paragraph for why the strongest rival wins. The build/buy/partner/retire decision remains a stronger forcing function than the article alone. |
| **4. Customer-discovery interviews** (who+where, past-behavior questions, bias audit, per-interview debrief, 5-interview cadence, asymmetry) | `templates/interview-plan.md` wired into P4; `$discover-interview-synthesis` conditional when raw interviews exist; assumption provenance fields feed `doctor` | **Landed, deliberately advisory** | The kit still allows an explicit waiver/no-user path, but it no longer lets that become invisible. Skipping real users must be recorded as an assumption/risk so the confirmation-bias watch can surface it before gates. |
| **5. Stress-test solution design** (3 load-bearing assumptions + cheapest refutation; "solving validated problem or original?") | `red-team-strategy.md`; `$assumption-challenger`; P5 feature-add bar; P6 validation-prototype evidence-vs-hypothesis section | **Landed** | The kit ranks load-bearing assumptions, asks for cheapest tests/kill criteria, and now explicitly checks whether requirements and the prototype are solving the validated problem rather than the original assumption. |
| **6. Smallest validation prototype** (ONE core interaction → 5 target users → go/no-go) | P6 Validation Prototype: single core interaction, throwaway scope, ~5 target users, observed behavior, PMF signals, pivot diagnostics, waivable with rationale | **Landed** | This is now its own phase before architecture/full build. The gate sequence is Product Gate P5 -> P6 validation -> Architecture Gate P7. |

## Infrastructure the article doesn't even mention (pipeline strengths to preserve)

- **Persistent assumption + risk registers** carried across all 10 phases — better than the article's per-interview debrief alone.
- **Existing-solutions-scan with a forced build/buy/partner/retire User Decision** that *blocks P2 completion while pending* — a structural "don't build what you should just buy" guard the article only implies.
- **Four human gates** + light/strict approval modes.
- **`$utility-pm-critic` run in a fresh context** against the finished PRD — a built-in fresh-eyes red-team.
- **`doctor` health check** for state/deliverable consistency.
- **Engineering rigor downstream** (TDD, systematic-debugging, verification-before-completion, code-review skills) for P8/P9.

## One-line synthesis

The pipeline originally encoded ~70% of the article's methodology. After the
Founder's-Playbook increment, the in-scope Idea + MVP method is structurally
landed: falsifiable hypothesis, 4-layer competition, required red-team moments,
customer-discovery planning, evidence provenance, P6 validation prototype, PMF
signals, and gate-surfaced bias warnings. The remaining boundary is deliberate:
Launch/Scale operating-system work is outside this 0->1 validation/build kit.
