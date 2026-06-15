# 02 — Source Research: the full Founder's Playbook (beyond the Idea stage)

## Source & provenance

- **Primary:** *The Founder's Playbook: Building an AI-Native Startup* — Anthropic/Claude, **published 2026-05-14**, ~36-page guide. Landing page: <https://claude.com/blog/the-founders-playbook> (announcement only; full content is a downloadable PDF).
- **Confirmed by the official page:** four stages — **Idea → MVP → Launch → Scale** — plus a **product-usage matrix** (when/how to use Claude *Chat*, *Cowork*, *Code* per stage) and founder case studies (Ambral, Anything, Carta Healthcare, HumanLayer, Vulcan Technologies).
- **Official one-line scope per stage:** Idea = "validate a problem hypothesis, map a competitive landscape, and run customer discovery with AI"; MVP = "architecture, scope, and security practices for AI-generated codebases"; Launch = "a Launch-stage operating system that replaces founder attention with agentic workflows"; Scale = moats & exit.
- **Detail below** is from a credible third-party close-reading of the PDF (note.com / KiKi@AIx, 2-part) cross-checked against TechTimes/Medium analyses. **Confidence: medium-high on substance, not verified line-by-line against the primary PDF.** Treat specific numbers (e.g. Sean Ellis 40%) as as-reported.
- The user-supplied article = the **Idea stage** only (already captured in [00](00-article-methodology.md)). Everything below is **complementary** material the article did not cover.

## Why this matters for us

The playbook's honest thesis — *"reach problem-solution fit before touching a codebase, and AI makes it dangerously easy to skip that step"* — **is literally our project's reason to exist** (shift-left, block code until validated). The playbook is external third-party validation of the kit's premise. Its MVP/Launch/Scale stages map onto our **P5–P9**, so they're a rich source of concrete increments.

---

## MVP stage → maps to our P5 / P6 / P7 / P8

A 7-step MVP procedure. Dual goal: *"build the minimum version real users adopt"* + *"move fast without accumulating technical debt"* (in the AI era speed is the only variable, so debt snowballs).

1. **Architecture before building → a persistent `CLAUDE.md`.** Capture: what you're building (core problem/users/scale), realistic 6-month scale, design principles, dependencies to avoid, trade-offs consciously accepted. *Persistent project memory for all later decisions.*
2. **Define & protect scope.** Three elements: core deliverables; **what explicitly NOT to do**; feature-add criterion = *"What concrete evidence from actual users justifies adding this?"* Use Claude as validator: *"Is this real user signal or founder enthusiasm disguised as product thinking?"*
3. **Build sessions execute pre-made decisions, don't introduce new ones.** Each session: review scope → load `CLAUDE.md` → **update it post-session** (what was built / decisions / assumptions). *"Five minutes of documentation per session is cheap insurance against architectural drift."*
4. **Security review BEFORE any user touches it.** Auth & session management; API response info leakage; input validation / injection; dependencies with known CVEs. *"Agentic coding tools generate code that works, not code that is inherently secure… a security review before any user touches your app is the minimum responsible threshold for releasing an MVP."*
5. **Measurement framework pre-launch.** Define retention baseline + Day-7 / Day-30 targets *before first users*. Then ask Claude: *"What would a skeptic say about these numbers?"*
6. **Manage discovery & feedback.** Cowork handles logistics (contact lists, scheduling, bug triage); **humans retain control over interpreting feedback** (core need vs nice-to-have, which segment, early-adopter artifact?).
7. **Iterate toward evidence, not perfection.** PMF instruments:
   - **Sean Ellis Test** — ask active users *"How would you feel if you could no longer use this?"* ≥**40% "very disappointed"** ⇒ meaningful PMF.
   - **Effort Test** — pre-PMF needs constant founder pushing; post-PMF the product is *pulled*. The push→pull shift is the clearest signal.
   - **Exit criteria MVP→Launch = the three R's:** **Retention** (return), **Revenue** (pay), **Referral** (tell others) — need genuine evidence of ≥1.

**Go/No-Go — three pivot questions** (if no meaningful progress after 3 iterations): (a) is a *sub-segment* reacting differently (look at sub-groups, not aggregate)? (b) is the designed-vs-actual-value gap a *messaging* or a *product* problem? (c) what must be true for PMF, and is that realistic (if impossible → pivot)?

**Four MVP pitfalls:** technical debt from agentic coding (AI re-derives foundations each session → drift); **false PMF** (friends/investors/HN spikes don't predict weeks 6–12 retention); **frictionless scope creep** (when a feature costs half a day, the old time-brake is gone); **security vulnerability** (works ≠ secure; no feedback until attacked).

**Explicit principle:** *"Using Claude as a structured devil's advocate is a core use case at **every** stage."* (confirms the Idea-stage article's central claim).

---

## Launch stage → maps to our P8 / P9 (+ ops, partly out of scope)

- **Exit criteria (all three at once):** (1) repeatable growth — CAC, LTV, payback understood per channel; (2) product withstands production load — infra/security/compliance stable; (3) operations run **without the founder as bottleneck**.
- **Technical-debt remediation:** full **design audit with Claude Code** → triage into **pre-release fix / next-cycle / acceptable debt** → record decisions into `CLAUDE.md`.
- **Security & compliance = continuous** (SOC 2 / GDPR / HIPAA code-level audits), *"a continuous development-cycle task, not a one-time project."*
- **Founder-bottleneck elimination:** inventory repetitive tasks → categorize full-automation / human-delegable / founder-only-judgment → design workflow logic. *(Ops automation — largely outside a coding pipeline's scope.)*
- **Launch pitfalls:** debt compounds; founder stays the constraint; security/compliance deferred; **premature scaling kills PMF clarity**.

## Scale stage → maps to our P2 (right-to-win) and P9 (continue/scale decision)

- **Three moat types:** (1) **proprietary knowledge substrate** (codified expert workflows compound into non-replicable depth); (2) **user-data advantage** (time-locked, context-specific behavioral fingerprints competitors can't buy); (3) **workflow lock-in** (APIs/webhooks/SDKs make switching a company-wide project).
- **Moat-validation question:** *"If a well-funded incumbent copied your product today, would your users stay?"* If no → moat insufficient; deepen knowledge/data/workflow. (Crisp complement to our P2 "right to win.")
- **Exit = sustainable profitability / IPO-readiness / acquisition.**

## Product-usage matrix (philosophical alignment, low direct relevance)

Chat (strategy, narrative, segmentation) ↔ Cowork (ops, logistics, GTM execution) ↔ Code (audit, hardening, infra). *"Each tool's outputs become inputs for the other two; results compound."* — same spirit as our markdown source-of-truth, but our kit is deliberately agent-agnostic, so we won't hard-wire product names.

---

## Complementary points worth harvesting (ranked by fit to our pipeline)

| # | Point (from MVP/Launch/Scale) | Maps to | Fit |
|---|---|---|---|
| C1 | **Scope-protection doc**: explicit non-goals + evidence-gated feature-add rule ("real user signal or founder enthusiasm?") | P5 PRD / P7 | **High** — cheap, fights scope creep, on-brand with shift-left |
| C2 | **Pre-release security review** as a required threshold (auth, leakage, injection, vuln deps) | P8 (or P6/P7) | **High** — concrete, named, currently not a required gate step |
| C3 | **PMF instruments**: Sean Ellis 40% test, Effort (push→pull) test, three R's as exit criteria | P9 / outcome-review + a pre-build validation step | **High** — turns "outcome review" into measurable go/no-go |
| C4 | **Architectural-memory discipline**: a per-project memory doc updated each build session ("insurance against drift") | P6→P8 | **Medium-high** — aligns with source-of-truth; partly via ADRs already |
| C5 | **"Skeptic check" on your own metrics** ("what would a skeptic say about these numbers?") | P5 instrumentation, P9 | **Medium-high** — a one-line disconfirmation guard |
| C6 | **Three pivot/diagnostic questions** (sub-segment? messaging vs product? what must be true?) | P9 iterate-pivot-decision | **Medium** — enriches an existing template |
| C7 | **Moat-validation question** + three moat types | P2 right-to-win / P9 | **Medium** — sharpens existing "right to win" |
| C8 | **False-PMF / early-traction skepticism** (friends/investors/HN ≠ retention) | P9, validation step | **Medium** — a named trap to encode as a check |
| C9 | **Design-audit + 3-bucket debt triage** before release | P8 | **Medium** — we have code-review skills; triage bucketing is the add |
| C10 | "Structured devil's advocate at **every** stage" is the explicit core principle | cross-cutting | **High** — mandate, not just confirm, the adversary everywhere |
