# 04 — Incremental Development Plan

> Derived from [03 decisions](03-gap-analysis-and-decisions.md). Grounded in the real engine: recipes' `outputs:` drive required-artifact checks (`phase_outputs`/`stage_complete`), `gate_precondition_errors()` enforces content preconditions (e.g. the P2 "User Decision: pending" block), and `doctor()` + `validate_state_invariants()` report consistency. Increments are template/recipe/register-first; only G8 touches the engine.

## Engine constraints to respect (discovered, not assumed)

1. **Registers use a custom parser** (`parse_register` in `pipeline.py`, "lightweight `- id:` registers without PyYAML"). The assumption entry already has an `evidence: []` field. **Keep new fields flat** under each `- id:` item, or extend `parse_register` in the same PR — nested YAML may not parse.
2. **Make an artifact required** by adding its path to a recipe's `outputs:` and shipping its template. `stage_complete` hashes outputs and refuses completion if missing.
3. **Gate preconditions** hook in `gate_precondition_errors(gate)` (already special-cases P2 scan + P5 PRD hashes). New "before this gate, X must be true" checks go here.
4. **Four-copy sync** ([[four-copy-sync]]): edit canonical (`skills/…`, `pipeline-template/.pipeline/vendor/…`, `recipes/`, `templates/`, `state/`), then `python3 scripts/sync_bundled_copies.py --write`. Never hand-edit the `agent-adapters/hermes|openclaw` mirrors.
5. **Agent-agnostic phrasing** in all skills/templates — describe the activity ("web search from the agent runtime", "have your agent argue against this"), never "use Claude Cowork".
6. **Test loop** per change: `pipeline.py status`, `pipeline.py doctor`, and run the affected `pipeline.py run P<n>` against the dogfood docs.

---

## TIER 1 — cheap, high-leverage, sharpen existing artifacts (template/recipe only)

### T1.1 — Sharpen the idea brief into a falsifiable hypothesis  *(G5)*
- **File:** `pipeline-template/.pipeline/templates/idea-brief.md`
- **Change:** Add near the top a single required line and two fields:
  - `## Falsifiable hypothesis` — `[persona] in [scenario] every [frequency] hits [problem] because [cause], costing [quantified loss].`
  - Add `## Frequency` and `## Current workaround (and where it hurts)` (the article's missing dimensions).
- **Why:** anchors all downstream P2 research/queries to one testable claim instead of a vague observation.
- **Accept:** P1 output contains a one-sentence hypothesis with persona+frequency+quantified loss; P2 existing-solutions-scan queries can be generated from it.
- **Effort:** XS.

### T1.2 — Upgrade the existing-solutions scan to the 4-layer + review-mining + steelman model  *(G4)*
- **Files:** `skills/idea2product-p2-strategy-analysis/SKILL.md` (the `### Search` + `## Output` blocks) and a new/extended scan structure.
- **Changes:**
  - Search section: explicitly require **four layers** — ① direct ② indirect/substitute ③ **potential acquirers** (incumbents with adjacent capability) ④ **adjacent movers** (could enter).
  - Add a required sub-step **"Competitor review mining"**: pull recurring complaints (App Store / G2 / Reddit / forums) → top-5 pains table → mark which the hypothesis addresses vs. which were unanticipated.
  - Add a required **"Steelman the strongest rival"** paragraph: the most persuasive case for *why they win and we fail*, and whether our differentiation is an actual moat.
  - Extend the scan template's `## Candidate Solutions` table with a `Layer` column; add `## Competitor Pain Mining` and `## Steelman` sections.
- **Why:** the article's "competitor blindness" fix; turns a list into evidence + an honest threat read.
- **Accept:** scan shows ≥1 candidate per layer (or explicit "none found"), a top-5 pain table with source URLs, and a steelman paragraph.
- **Effort:** S.

### T1.3 — PRD non-goals + evidence-gated feature-add  *(G6, G11)*
- **Files:** `pipeline-template/.pipeline/vendor/product/deliver-prd/SKILL.md` (+ its `references/TEMPLATE.md`).
- **Changes:** add two required PRD sections:
  - `## Non-goals (what this product will intentionally NOT do)`
  - `## Feature-add bar` — every candidate feature must answer *"What concrete evidence from real users justifies this?"* and pass the check *"real user signal, or founder enthusiasm?"*
  - One line folding in G11: *"Confirm each requirement traces to the problem **validation revealed**, not the one assumed at P1."*
- **Why:** anti-scope-creep is already in the README's value prop; this operationalizes it. Frictionless scope creep is the named MVP pitfall.
- **Accept:** PRD has non-empty Non-goals; each P0/P1 feature cites an evidence basis.
- **Effort:** S.

### T1.4 — Make the adversary required at P2 and P4; add a "skeptic check"  *(G1, C5)*
- **Files:** `recipes/p2-strategy-analysis.yaml`, `recipes/p4-product-discovery.yaml`; small template note in `measure-instrumentation-spec` usage / `outcome-review.md`.
- **Changes:**
  - P2 & P4 recipes: promote `$assumption-challenger` from optional → a **required `non_skill_process` red-team checkpoint** (one pre-mortem pass per phase), mirroring P3's pattern.
  - Add a reusable one-liner to instrumentation/outcome templates: *"Skeptic check — what would a skeptic say about these numbers/this evidence? Record the strongest objection."*
- **Why:** playbook states devil's advocate is core "at every stage"; today it's mandatory only at P1.
- **Accept:** P2 & P4 cannot complete without a recorded red-team note; instrumentation/outcome docs contain a skeptic-objection line.
- **Effort:** S.

### T1.5 — Moat-validation question  *(G10)*
- **Files:** `templates/decision-memo.md` (P3) and `templates/outcome-review.md` (P9); optional mention in `$ceo-advisor`/strategy note.
- **Change:** add `## Moat check` — *"If a well-funded incumbent shipped your product today, would users stay? Why?"* with the three moat types (proprietary knowledge / data advantage / workflow lock-in) as prompts.
- **Why:** sharpens the existing "right to win" with a crisp, memorable test.
- **Effort:** XS.

---

## TIER 2 — the core value: make real-user evidence first-class & checkable

### T2.1 — New vendored skill: `discover-interview-plan` (customer discovery)  *(G2)*
- **New files:** `pipeline-template/.pipeline/vendor/product/discover-interview-plan/SKILL.md` (+ `references/TEMPLATE.md`, `EXAMPLE.md`), following the PM-Skills format already used by `discover-interview-synthesis`.
- **Covers the article's Step 4 end-to-end:**
  1. **Who + where** — ideal-interviewee persona (title/company/team size), which seniority feels the pain most, where they congregate (communities, LinkedIn/Slack, conferences), priority order.
  2. **Question bank, bias-audited** — draft questions, then flag **leading / too-broad / socially-desirable** ones and rewrite to probe **past behavior** ("tell me about the last time…") not future intent ("would you use…"); design follow-up probes for the 2–3 likely-dodged moments.
  3. **Per-interview debrief format** — confirmed / challenged / surprised / *"am I reading this for what I want to hear?"*.
  4. **Cadence + asymmetry guard** — synthesize every 5; if the "supports" list >> "challenges" list, flag and investigate.
- **Wiring:** add `$discover-interview-plan` to `recipes/p4-product-discovery.yaml` (and reference from P2 for problem-interviews). Output: `docs/20-product/interview-plan.md`.
- **Pair with the waiver rule (T2.2).**
- **Effort:** M.

### T2.2 — "No silent zero-evidence" rule: require user-contact evidence or an explicit, recorded waiver  *(G2, G8)*
- **Files:** `recipes/p4` outputs + `gate_precondition_errors('product')` in `pipeline.py`.
- **Change:** before the **Product Gate**, require either (a) an interview-synthesis artifact with N≥ a small floor (e.g. 3–5), or (b) an explicit waiver recorded in the assumption-register (`status: assumed`, `validation_method: none`, owner + reason). The gate message names the choice; it never *blocks forever*, but it **forces the founder to consciously acknowledge building on zero user contact** — exactly the "exquisite self-deception" the article warns about.
- **Why:** the pipeline today can reach a Product Gate with zero real conversations; this makes that a deliberate, logged decision.
- **Accept:** Product Gate request prints an error/notice unless interview evidence or a recorded waiver exists.
- **Effort:** M (engine).

### T2.3 — Evidence provenance + asymmetry in the assumption register + doctor checks  *(G8 — flagship)*
- **Files:** `state/assumption-register.yaml` (schema), `parse_register` + `doctor` + `validate_state_invariants` in `pipeline.py`, and the template/doc that explains the register.
- **Changes (keep parser-compatible — flat fields under each `- id:`):**
  - Extend each assumption with: `validation_method: [user_interview|experiment|desk_research|founder_belief|none]`, `user_contact_n: <int>`, `evidence_for: <int>`, `evidence_against: <int>`, `confidence: [high|med|low]`. (Keep `evidence: []` for free-text/links.)
  - Extend `parse_register` to read the new flat fields.
  - **Doctor checks** (warnings, not hard blocks): (i) assumption `status: validated` but `validation_method` ∈ {desk_research, founder_belief, none} → *"validated without user contact"*; (ii) `evidence_against == 0` on a `validated` desirability assumption → *"no disconfirming evidence sought"*; (iii) `evidence_for` ≫ `evidence_against` across the register → *"confirmation-asymmetry: you may be collecting only supporting evidence."*
- **Why:** this is the unique-to-us move — it encodes *"confirmation bias now has a research engine"* as a **guardrail the doctor enforces**, leveraging our persistent state (something prose playbooks cannot do).
- **Accept:** `doctor` surfaces the three warnings on a register that has validated-but-unsupported or lopsided assumptions; clean on a balanced one.
- **Effort:** M (engine).

### T2.4 — Required pre-release security review  *(G7)*
- **Files:** `recipes/p8-build-release.yaml` (+ `templates/launch-gtm-checklist.md` or a new `security-review.md`), optional wire to the host `security-review` skill.
- **Change:** add a required `non_skill_process` + output: a **pre-release security review** covering auth/session, API response info-leakage, input validation/injection, dependencies with known CVEs. Gate it as a **Release Gate precondition** (`gate_precondition_errors('release')`).
- **Why:** "agentic coding generates code that works, not code that's secure"; playbook calls a pre-user security review the *minimum responsible threshold*.
- **Accept:** Release Gate cannot be requested without a completed `security-review.md`; the four checks each have a status.
- **Effort:** S–M.

---

## TIER 3 — structural: the pre-build validation prototype + PMF go/no-go

### T3.1 — Lightweight "validation prototype" step (one core interaction → ~5 users)  *(G3)*
- **Design options (pick one — needs a short decision):**
  - **(A) New optional sub-phase P5.5 / "P-validate"** between Product Definition and Architecture: define the **single core, indispensable interaction**; build the smallest possible version; put it in front of **~5 target-persona users**; record reactions → go/no-go. Distinct from heavyweight `$measure-experiment-design` (which stays for traffic-rich A/B).
  - **(B) A required `non_skill_process` inside P4/P5** producing `docs/20-product/validation-prototype-plan.md` + results, without a new phase number (less engine change).
- **Recommendation:** start with **(B)** (lower risk, no state-machine change), graduate to (A) if users want a hard gate. Reuse `$assumption-challenger`'s concierge/fake-door/usability techniques + the new PMF instruments (T3.2).
- **Why:** the article's Step 6 and the playbook's whole MVP ethos: *the prototype is not evidence; the conversations are.*
- **Effort:** M (B) / L (A).

### T3.2 — PMF instruments + pivot diagnostics in outcome-review & pivot-decision  *(G9)*
- **Files:** `templates/outcome-review.md`, `$iterate-pivot-decision` usage, `recipes/p9`.
- **Changes:** add to outcome-review: **Sean Ellis test** (≥40% "very disappointed"), **Effort test** (founder pushing vs product pulled), **three R's** (Retention/Revenue/Referral) as the MVP→Launch exit criteria, and the **false-PMF caution** (friends/investors/HN ≠ weeks-6–12 retention). Add the **three pivot diagnostics** (sub-segment differs? messaging vs product? what must be true for PMF — realistic?) to the pivot-decision step.
- **Accept:** outcome-review captures at least one PMF instrument with a target; pivot decisions answer the three diagnostics.
- **Effort:** S–M.

### T3.3 — (Light) post-build architecture-memory nudge  *(G12)*
- **File:** `recipes/p8` / executing-plans usage note.
- **Change:** one line — *"After each build session, update the architecture/decision notes (ADR or design-rationale) with what was built, decisions made, assumptions set — cheap insurance against drift."* No new artifact.
- **Effort:** XS.

---

## Recommended sequencing

1. **Ship Tier 1 as one PR** (T1.1–T1.5) — all template/recipe/skill-prose, no engine risk, immediately sharpens every run. Run sync + doctor + a dogfood P1–P4 pass.
2. **Ship T2.3 (evidence provenance + doctor)** next — the flagship; isolated to register + pipeline.py; add unit-ish tests by crafting a register fixture and asserting doctor output.
3. **Ship T2.1 + T2.2 together** — interview-plan skill + the Product-Gate evidence/waiver rule.
4. **Ship T2.4** — security review at Release Gate.
5. **Tier 3** — decide T3.1 option (B vs A) with the user; then T3.2, T3.3.

## Cross-cutting acceptance / rollout

- Every skill/template/recipe edit → `scripts/sync_bundled_copies.py --write`; confirm hermes/openclaw mirrors updated; `git status` clean of stray edits to mirrors.
- `pipeline.py doctor` and `status` pass after each tier on the dogfood workspace.
- Update `README.md` / `README.zh-CN.md` phase table + `docs/TECHNICAL-DEEP-DIVE.md` where new outputs/gate preconditions are introduced (esp. T2.2, T2.4, T3.1-A).
- Keep all new prose **agent-agnostic**; no Claude product names.

## Risks & open questions

- **R1 — register parser fragility:** new fields must extend `parse_register` in the same change or stay flat; add a fixture test. *(T2.3)*
- **R2 — gate friction:** T2.2/T2.4 add gate preconditions; keep them as *"provide evidence OR record an explicit waiver/decision"* so the pipeline never hard-stops a determined solo founder — it forces a *conscious* choice, matching the kit's light-gate default.
- **R3 — scope of T3.1:** a new phase (option A) is a real state-machine change (phase numbering, `pipeline-state.yaml`, docs). Prefer option B first.
- **Q1 — for the user:** Tier-3 prototype — **new phase (A)** or **in-phase step (B)**?
- **Q2 — for the user:** interview-evidence floor for the Product Gate — hard minimum (e.g. N≥3) or pure waiver-with-rationale?
