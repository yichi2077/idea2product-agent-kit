# 06 — Occam Development Plan (necessity × done)

> Decision rule (yours):
> - **Not done + necessary → DO FIRST.**
> - **Done + necessary → KEEP & HARDEN (固化).**
> - **Not done + unnecessary → DON'T DO.**
> - **Done + unnecessary → keep for now (暂时保留); don't spend churn ripping it out.**
>
> Necessity test (first principles): does it raise P(avoid building something nobody wants) **and** is it something **only structure can enforce**, at cost proportional to value? The kit's edge is *lightweight* enforced discipline — every required entity is taxed against cumulative weight.

## Classification

| Item | Done? | Necessary? | Quadrant → Action |
|---|---|---|---|
| Falsifiable-hypothesis fields (idea-brief) | ✅ | ✅ | **Keep & harden** |
| PRD non-goals + evidence-gated feature-add | ✅ | ✅ | **Keep & harden** |
| Competitor **review-mining + steelman** | ✅ | ✅ | **Keep & harden** |
| Skeptic-check line (outcome-review) | ✅ | ✅ | **Keep & harden** |
| New **P6 validation-prototype phase** (concept) | ✅ | ✅ | **Keep & harden** |
| **T2.3** evidence-provenance fields + `doctor` confirmation-bias warnings | ❌ | ✅✅ (flagship, unique to us) | **DO FIRST** |
| **T3.2** PMF instruments (Sean Ellis 40% / effort / three R's) | ❌ | ✅ | **DO** (cheap) |
| **T2.1** customer-discovery interview guide | ❌ | ✅ (thinnest seam) | **DO — as a template, NOT a new skill** |
| T2.2 Product-Gate evidence/waiver nudge | ❌ | ➖ (overlaps T2.3 doctor) | **DO minimal** — one advisory line, no new precondition engine |
| 4-layer scan: layers 3–4 (acquirers/adjacent) | ✅ | ➖ (marginal for solo MVP) | **暂时保留** (optional: mark L3–4 "deep-dive optional") |
| Required red-team at **P2** | ✅ | ➖ (P3 already red-teams strategy) | **暂时保留** (optional: → "recommended") |
| Required red-team at **P4** | ✅ | ➖ (P5 pm-critic covers it downstream) | **暂时保留** (optional: → "recommended") |
| Moat check (P3/P9) | ✅ | ➖ (premature for 0→1; Scale-stage) | **暂时保留** (optional: → one optional prompt) |
| Clean renumber P1→P10 (execution choice) | ✅ | ➖ (aesthetic > first-principles) | **暂时保留** (sunk; rolling back = more churn) |
| T2.4 pre-release security review (as required gate) | ❌ | ➖ (quality gate, off the "nobody-wants" thesis; P9 build skills partly cover) | **DON'T DO now** (offer later as *optional* conditional skill, never a required gate) |
| T3.3 post-build architecture-memory nudge | ❌ | ✖ (redundant with ADRs) | **DON'T DO** |

## The plan

### Phase A — DO FIRST (necessary, not done)

**A1 — T2.3 evidence provenance + `doctor` confirmation-bias guard (flagship).**
- `state/assumption-register.yaml`: add flat fields per assumption — `validation_method: [user_interview|experiment|desk_research|founder_belief|none]`, `user_contact_n: <int>`, `evidence_for: <int>`, `evidence_against: <int>`, `confidence: [high|med|low]`. Seed A-0001 accordingly.
- `pipeline.py`: extend `REGISTER_KEYS` + `parse_register` to read the new flat fields (verify the parser first — it only keeps known keys).
- `pipeline.py` `doctor`: emit **non-blocking warnings** — (i) `status: validated/closed` but `validation_method ∈ {desk_research, founder_belief, none}` → "validated without user contact"; (ii) a desirability assumption marked validated with `evidence_against == 0` → "no disconfirming evidence sought"; (iii) Σ`evidence_for` ≫ Σ`evidence_against` across the register → "confirmation asymmetry — you may be collecting only supporting evidence."
- Doc the fields in `PIPELINE-USER-GUIDE.md`.
- **Accept:** crafted register triggers all 3 warnings; balanced register is clean; existing flows unchanged; `doctor` still exits 0 (warnings, not errors).
- **Why first:** converts the article's core warning into a guardrail *only persistent state can enforce* — the single most first-principles, most differentiated gain.

**A2 — T3.2 PMF instruments (cheap, high signal).**
- `templates/outcome-review.md` + `templates/validation-prototype.md`: add **Sean Ellis test** (≥40% "very disappointed"), **effort test** (founder pushing vs product pulled), **three R's** (Retention/Revenue/Referral) as the go/no-go criteria.
- **Accept:** both templates carry the instruments as fillable sections with targets.

**A3 — T2.1 customer-discovery as a TEMPLATE (Occam: no new skill).**
- New `templates/interview-plan.md`: who + where they congregate; bias-audited question bank (flag leading / socially-desirable; rewrite to **past behavior** not future intent); per-interview debrief; synthesize every 5; confirm/challenge **asymmetry** guard.
- Wire into `recipes/p4-product-discovery.yaml` as a `non_skill_process` step; reuse existing `$discover-interview-synthesis` for synthesis. **No new skill entity.**
- **Accept:** template exists + referenced by P4; zero new skills added.

**A4 — Product-Gate nudge (minimal).**
- One advisory line in the existing product-gate output when no user-contact evidence and no recorded waiver exists. **No new precondition logic** (the A1 doctor warning is the real guard). Drop entirely if A1+A3 feel sufficient.

### Phase B — KEEP & HARDEN (necessary, done) — light only

- **B1:** add a short `CHANGELOG.md` entry making the kept Tier-1 behaviors + new P6 official.
- **B2:** fill `references/EXAMPLE` for the new P6 validation-prototype template so agents have a concrete reference.
- **B3:** rely on existing `sync --check` for drift; **do not** build content-validators (that would itself violate Occam).

### DON'T DO (unnecessary, not done)
- **T3.3** architecture-memory nudge — redundant with ADRs.
- **T2.4** security review **as a required gate** — off-thesis; if ever wanted, ship as an *optional* conditional skill only.

### 暂时保留 (unnecessary, done) — no action now
Moat check · 4-layer L3–L4 · required red-team at P2 & P4 · clean renumber. Keep as-is. *Optional, cheap, future* simplifications if the kit feels heavy: downgrade P2/P4 red-team and moat from required → recommended; mark competitor layers 3–4 optional. Not prioritized (per the rule: don't churn done work).

## Cumulative-weight discipline (the meta-rule going forward)
Every new **required** entity (phase, gate, required step, required field) is taxed against the kit's "lightweight" moat. Default new things to **optional/recommended/template**; promote to **required** only when (a) it raises P(avoid building nobody-wants) and (b) only structure can enforce it. A1 is the model: maximal leverage from a guard the engine alone can run.
