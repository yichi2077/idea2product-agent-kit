# 03 — Gap Analysis & Decisions (what to internalize, what to decline)

> Synthesis of [00 article](00-article-methodology.md) + [01 capability map](01-pipeline-capability-map.md) + [02 source research](02-source-research.md).
> Lens: does an increment **strengthen the kit's core mission** (force disconfirmation + real evidence before code, locally, agent-agnostically) at acceptable effort and fit? I recommend, with reasons; the call on what to build is yours.

## Decision principles applied

1. **On-mission > novel.** The kit's edge is *enforced disconfirmation + persistent evidence state*. Increments that make that discipline **mandatory and measurable** beat new content.
2. **Leverage what only we can do.** The article/playbook are prose; we have **persistent registers + gates + a doctor**. The highest-value moves encode their advice as *state we can check*, not more markdown to read.
3. **Agent-agnostic.** Do not hard-wire Claude product names (Chat/Cowork/Code). Keep skills portable across Cursor/Codex/etc.
4. **Respect scope boundaries.** The kit is a 0→1 validation+build pipeline, **not** an ops-automation / founder-attention / compliance-program tool. Decline Launch/Scale ops material.
5. **Cheap, reversible, template-first.** Prefer recipe/template/register edits over engine rewrites. Mind the **four-copy sync** ([[four-copy-sync]]).

## Gap register (consolidated, prioritized)

| ID | Gap | Source | Mission value | Effort | Decision |
|----|-----|--------|---------------|--------|----------|
| **G1** | Disconfirmation/red-team is **required only at P1**; optional/absent at P2 & P4; no "skeptic-check your own numbers" | Article §2; Playbook ("devil's advocate at every stage") | High | Low | **ADOPT (Tier 1)** |
| **G2** | **Customer-discovery interviews not first-class**: no who/where targeting, no bias-audited question bank, no past-behavior framing, no per-interview debrief, no 5-interview cadence, no confirm/challenge asymmetry guard; synthesis is conditional & synthesis-only | Article §4; Playbook Idea pillar "run customer discovery with AI" | **Highest** | Med | **ADOPT (Tier 2)** |
| **G3** | No **lightweight pre-build validation prototype** (one core interaction → ~5 users → go/no-go); existing experiment skill is heavyweight A/B; results measured only at P9 | Article §6; Playbook MVP step 7 + three R's | High | Med-High | **ADOPT (Tier 3, phased)** |
| **G4** | Competitive scan lacks **4-layer model** (potential acquirers + adjacent movers), **competitor-review mining** (top-5 pains from G2/Reddit/App Store), **steelman-the-rival** | Article §3 | Med-High | Low | **ADOPT (Tier 1)** |
| **G5** | Idea brief not framed as a **falsifiable hypothesis** (missing frequency + quantified severity + current workaround); rigorous hypothesis skill sits late in P4 | Article §1 | Med | Low | **ADOPT (Tier 1)** |
| **G6** | PRD lacks explicit **non-goals / won't-do** + **evidence-gated feature-add** rule ("real user signal or founder enthusiasm?") | Playbook MVP step 2 | High | Low | **ADOPT (Tier 1)** |
| **G7** | **No required pre-release security review** (auth, API leakage, injection, vulnerable deps) — "works ≠ secure" | Playbook MVP step 4 | High | Low-Med | **ADOPT (Tier 2)** |
| **G8** | Registers don't track **evidence provenance** (validated by N real users vs AI desk-research vs belief) or **evidence-for vs -against asymmetry**; doctor can't flag "validated without disconfirmation / without user contact" | Article §2/§4 (confirmation bias); our own infra | **Highest (unique leverage)** | Med | **ADOPT (Tier 2)** |
| **G9** | Outcome/pivot lacks concrete **PMF instruments** (Sean Ellis 40%, effort push→pull, three R's) and **three pivot diagnostics**; false-PMF trap not encoded | Playbook MVP step 7 + Go/No-Go | Med-High | Low-Med | **ADOPT (Tier 3)** |
| **G10** | No **moat-validation question** ("if a well-funded incumbent copied you today, would users stay?") / moat typology in strategy & outcome | Playbook Scale | Med | Low | **ADOPT (Tier 1, light)** |
| **G11** | "Solving the **validated** problem or the **original** one?" reframing check absent before build | Article §5 | Med | Low | **ADOPT (fold into G2/G6)** |
| **G12** | Architectural-memory-updated-each-session discipline | Playbook MVP steps 1&3 | Low-Med | Low | **PARTIAL** — we already center markdown source-of-truth + ADRs; add only a one-line "update architecture notes post-build-session" nudge in P8. No new artifact. |

## Explicitly DECLINED (with rationale)

- **Founder-attention operating system / ops-automation inventory (Launch)** — outside a code-gen validation pipeline's scope; belongs to a separate ops tool. *Decline.*
- **Continuous compliance program management (SOC 2 / GDPR / HIPAA as an ongoing org function)** — we adopt the *pre-release security review* (G7) but not full compliance-program tooling. *Decline the program; keep the review.*
- **Scale-stage org build (HR/payroll/legal), GTM growth-engine staffing** — beyond 0→1. *Decline.*
- **Hard-wiring the Chat/Cowork/Code product matrix** — violates agent-agnostic principle. Keep the *philosophy* ("artifacts compound as inputs to the next phase") which we already embody. *Decline the wiring.*
- **A heavyweight statistical A/B mandate at idea stage** — the existing `$measure-experiment-design` stays for when traffic exists; for pre-build we add the *lightweight* G3 path instead. *Decline making A/B the default early.*

## The through-line

The single most valuable, most *us*-shaped move is **G8 + G2 together**: make **real-user evidence a tracked, first-class, checkable asset**, and let the **doctor flag confirmation-bias patterns** (assumptions marked validated with no disconfirming search and no user contact; lopsided evidence-for/against). That converts the article's best insight — *"confirmation bias now has a research engine"* — from a warning into a **guardrail the engine enforces**, which neither the article nor the playbook can do. G1/G4/G5/G6 are cheap Tier-1 wins that sharpen existing artifacts; G3/G7/G9 add the missing pre-build evidence + safety gates.
