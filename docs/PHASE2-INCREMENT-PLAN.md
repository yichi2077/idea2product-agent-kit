# Phase 2 Increment Plan — idea2product Agent Kit

Date: 2026-06-13
Status: DRAFT — pending owner approval
Inputs: repo audit (code + docs), external landscape research, Gemini audit memo (treated as advisory input, independently verified)

---

## 1. Value Assessment (审慎结论)

### 1.1 Where the kit is genuinely differentiated

The 2026 spec-driven-development (SDD) landscape is crowded downstream:
Spec Kit (greenfield spec→plan→tasks), BMAD (12+ persona simulated team),
OpenSpec (brownfield delta specs), Kiro, plus PM-side tools like ChatPRD.
Against that field, this kit's defensible position is:

1. **It owns the upstream that SDD tools skip.** Spec Kit starts at "feature
   specified"; BMAD starts at "we decided to build". P1–P5 (idea → strategy
   decision → product definition), with build/buy/partner/do-nothing comparison
   and a real-idea guard, is the part nobody in the SDD category does — and the
   kit *hands off into* Spec Kit at P7 instead of competing with it.
2. **Human-only gates are a real differentiator, not theater.** Challenge-code
   approval in an out-of-agent terminal + git tag audit trail directly addresses
   the "Excessive Agency" failure mode that persona-team frameworks (BMAD) are
   criticized for.
3. **Evidence-gated skills** (`$financial-analyst` / `$measure-experiment-results`
   only run on real data) are an unusually honest design in a category that
   routinely hallucinates market sizing.

### 1.2 Where the value is at risk

1. **The kit has never validated itself.** `pipeline-state.yaml` still reads
   `pilot_validation: PENDING_REAL_IDEA`; assumption A-0001 ("first real idea
   not supplied") is open. By the kit's own epistemic standard, its value is an
   unvalidated hypothesis.
2. **The market is moving toward iteration speed, not upfront analysis.**
   Solo-founder practice in 2026 is "ship in 1–2 weeks, iterate on real
   feedback". Standard mode budgets ~25 hours of analysis before a line of
   code. Light mode mitigates this, but the kit's center of gravity is still
   the funnel, not the loop.
3. **One-way state machine.** The pipeline has no `reopen`/rework verb. The #1
   documented failure mode of the whole SDD category is *spec drift* — stale
   upstream artifacts misleading downstream agents — and the kit currently has
   no mechanism to detect or propagate upstream changes.
4. **Artifact weight.** A Standard run produces 20+ markdown/YAML artifacts.
   The README's own warning ("without drowning in documents") is a live risk.

### 1.3 Verdict on the Gemini audit memo

| # | Gemini claim | Verdict | Notes |
|---|--------------|---------|-------|
| 1 | No feedback loop / rollback | **Correct — highest-value gap.** | `pipeline.py` has no revert verb; P9 says "reopen PRD or ADR" with no mechanism. Aligns with the category-wide spec-drift failure mode. |
| 2 | Empirical data integration too weak | **Directionally right, overstated.** | Kit already evidence-gates result skills and ships `$discover-interview-synthesis`. Real gap: no evidence *provenance* tracking and no intake convention. Building GA/DB connectors now would be over-engineering. |
| 3 | No LLM-as-judge quality gate | **Factually wrong as stated; real gap is enforcement.** | `$utility-pm-critic` (fresh-context PRD critique) is already a P5 required skill; Standard+ has cross-model red-team at P3. What's missing: the critique result is not machine-checked by `gate request` / `stage complete`. Note: LLM judges hit ~80–90% human agreement only with concrete rubrics; "score < 80 auto-reject" is not reliable enough to replace the human gate — wire it as a *precondition*, not a verdict. |
| 4 | No storytelling / pitch-deck output | **Valid but low priority for the ICP.** | The solo operator ships product first, pitches second. Must respect the single-source-of-truth principle: a deck is a *renderer* over decision-memo/PRD, never a new source artifact. |

### 1.4 Gaps Gemini missed

- **G1. Self-validation debt** (§1.2.1) — the most important one.
- **G2. Staleness/traceability enforcement**: `validate_handoff.py` only checks
  file existence; nothing detects "PRD changed after P7 packets were cut".
- **G3. Brownfield entry**: scaffold assumes empty repo; the common real case
  ("existing product, new feature/direction") has no documented entry at P4.
- **G4. Repo hygiene**: the repo's own `.pipeline/state/pipeline-state.yaml`
  ships an inconsistent state (`current_phase: P1` but product gate
  `awaiting_approval` with a live challenge) — leftover test state that the
  template copy does not have.
- **G5. Pipeline self-telemetry**: no record of phase wall-time or skill
  usefulness, so mode budgets in `pipeline-config.yaml` are unfalsifiable.

---

## 2. Phase 2 Scope (MoSCoW)

### Must

**M1. Pilot validation run (G1)**
Run one real idea end-to-end through P1→P3 (minimum) in Standard mode; record
a friction log (time per phase, artifacts actually read vs. written, skill
invocations that added nothing). Exit criteria: `pilot_validation` flipped,
A-0001 closed, friction log feeds M2/M3 scoping.
*This gates everything else — build no new mechanism before one real run.*

**M2. Iteration loop: `pipeline reopen` (Gemini #1, G2)**
- New verb: `pipeline.py reopen Px --reason "..."` — moves Px and all
  downstream phases out of `complete`, appends a rework entry to
  `decision-log.md`, and re-arms the affected gate (re-request required).
- Staleness detection: store a content hash of each phase's primary output at
  `stage complete`; `status`/`next` warn when an upstream artifact's hash no
  longer matches what a completed downstream phase consumed.
- Recipes gain an optional `rework_inputs` field so a reopened phase knows
  which downstream feedback artifact triggered it.
- Explicitly *not* automatic: agents may request reopen; only state-file
  mechanics are automated. No silent upstream rewrites.

**M3. Fix shipped state + state-machine invariants (G4)**
Reset the repo-root `.pipeline/state/` to template values; add a pytest
invariant check (gate cannot be `awaiting_approval` while its phase is not
complete) to `verify.sh`.

### Should

**S1. Critique-as-precondition wiring (Gemini #3, corrected)**
- `$utility-pm-critic` output becomes a structured artifact
  (`docs/20-product/pm-critic-report.md` + a scored rubric block).
- `gate request product` refuses unless the critic report exists, is newer
  than the PRD hash, and all rubric items are scored.
- Threshold behavior: configurable `warn` (default) vs `block`; the human
  approver always sees the score in the gate context. Same pattern applied to
  the P3 red-team artifact in Standard+.
- Anti-pattern guard: do not auto-reject on score alone (judge reliability),
  and do not let the same context that wrote the PRD score it.

**S2. Evidence provenance register (Gemini #2, right-sized)**
- Add `evidence_class: desk-research | real-data | interview | telemetry` and
  `source` fields to assumption-register entries and strategy/discovery
  templates.
- Define an `evidence/` intake convention (drop transcripts, CSV exports,
  analytics snapshots); `$discover-interview-synthesis` and
  `$measure-experiment-results` read from it.
- `pipeline status` surfaces the desk-research vs. real-data ratio per phase —
  making "坐而论道" visible instead of pretending to fix it with connectors.
- MCP connectors (GA, DB): document the integration point only; defer builds
  to Phase 3 pending pilot evidence of need.

**S3. Brownfield entry mode (G3)**
`install.py scaffold --brownfield` + a documented "start at P4 with an
existing product" path: P1–P3 collapse into a one-page current-state brief;
real-idea guard adapted accordingly.

### Could

**C1. Decision-memo / PRD one-pager renderer (Gemini #4)**
A `pipeline render` helper (or thin skill) that produces an exec one-pager or
deck from the decision memo and PRD via existing pptx/docx skills. Renderer
only — regenerable, never edited as a source. P3 and P8 outputs note its
availability.

**C2. Phase telemetry (G5)**
Record started/completed timestamps per phase in state; `status` shows actual
vs. budgeted minutes. Feeds future mode-budget tuning.

### Won't (this phase)

- Google Analytics / database / crawler connectors (revisit after pilot).
- Automatic agent-driven upstream rewrites on downstream feedback.
- Multi-idea portfolio state in one repo.
- "McKinsey-grade" slide system as a first-class pipeline phase.

---

## 3. Sequencing & exit criteria

1. **M3** (half-day) → 2. **M1** (1–2 weeks calendar, runs alongside) →
3. **M2** (the only substantial engineering item; design doc → ADR → build) →
4. **S1, S2** (each small once M2's hash plumbing exists) → 5. **S3, C1, C2**.

Phase 2 is done when: a real idea has passed Strategy Gate; `reopen` +
staleness warnings work end-to-end in tests; product gate refuses without a
fresh critic report; evidence provenance is visible in `status`.

## 4. References

- [Spec Kit vs BMAD vs OpenSpec (2026)](https://dev.to/willtorber/spec-kit-vs-bmad-vs-openspec-choosing-an-sdd-framework-in-2026-d3j) — spec drift as the category's #1 failure mode; framework strengths/weaknesses.
- [BMAD vs Spec Kit vs OpenSpec — Reenbit](https://reenbit.com/bmad-vs-spec-kit-vs-openspec-choosing-your-spec-driven-ai-framework/)
- [LLM-as-a-Judge practical guides — Confident AI](https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method), [Langfuse](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge) — rubric-anchored judging, ~80–90% human agreement, spot-check requirement.
- [ChatPRD](https://www.chatprd.ai/) — adjacent PM-tool positioning.
- [Solo Founder Index 2026 — ShipSquad](https://shipsquad.ai/blog/solo-founder-index-2026) — ship-fast-iterate norm for the ICP.
