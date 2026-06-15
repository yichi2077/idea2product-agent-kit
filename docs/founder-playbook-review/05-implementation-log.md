# 05 — Implementation Log

## Architecture check (your question: do phases have to be mutually exclusive? does the prototype step lack skill linkage?)

**Findings — investigated, not assumed:**

1. **There is no *codified* "mutually exclusive phases" principle.** A repo-wide grep for `mutually exclusive` / `互斥` / `one concern` / `separation of concern` / phase-boundary language found **nothing** in docs, recipes, or code. So the rule isn't written down.
2. **But the *de facto* design is real and strong.** Each phase has its own recipe, its own `outputs:`, its own thematic doc dir; the README sells *"focuses agent context only on the active phase"* (context isolation), and the WHY→WHAT→HOW split now runs P1-3 / P4-6 / P7-10, keeping phases single-concern. **Your instinct holds:** the candidate host phases (P4 discovery, P5 definition) are deliberately *pre-code thinking* phases — dropping a "build a throwaway + test on users" step inside them genuinely mixes validation-building into a definition phase and breaks the clean shift-left separation. **→ A dedicated phase is the correct call.**
3. **The engine treats every phase in `PHASES` as mandatory + strictly sequential.** At the time of the design decision, `pipeline.py` hardcoded P1..P9; after the increment it hardcodes P1..P10. `stage_complete` still only completes the current `ready` phase, rejects skips, and derives `next` by list index. **There is no "optional phase" concept.** So the new P6 became required for every project -> it is **waivable via a recorded "skip with rationale"** (mirrors the existing-solutions-scan `User Decision` pattern), honoring your "no hard floor / lightweight" choice.
4. **"This phase has no skill linkage" is NOT true.** A validation-prototype phase composes existing skills cleanly: **`$assumption-challenger`** already covers *"prototype before building,"* concierge/fake-door/usability tests, and *"measure behavior, not stated preference"*; plus `$measure-experiment-design` (when applicable) and the new PMF instruments (T3.2). So it links to skills — no orphan phase. A thin new *entry* skill (`idea2product-p*-validation-prototype`) is still worth adding for discoverability.

**Engine facts that make a new phase low-risk to add:**
- `recipe_path(phase)` resolves recipes by glob `{phase.lower()}-*.yaml` — any phase ID works.
- Doc dirs are thematic, **not** 1:1 with phase numbers — a new phase can write to a new dir (e.g. `docs/25-validation/`).
- Gates are keyed separately (`GATE_PHASES`); a new **non-gated** phase needs no gate wiring.
- Adapter skill mirrors exist only for **hermes + openclaw** (51 each); `sync_bundled_copies.py --write` regenerates them.

**Decision (made by user):** clean renumber to **P1..P10** — done (see Tier 3.1 below).

---

## Done — Tier 1 (shipped, verified: `doctor` healthy, recipes parse, sync clean)

All edits in **project-owned files** (no vendored-skill drift); propagated via `sync_bundled_copies.py --write`.

- **T1.1** `templates/idea-brief.md` — added **Falsifiable hypothesis** (persona/scenario/frequency/cause/quantified loss) + **Frequency** + **Current workaround** fields. *(G5)*
- **T1.2** `skills/idea2product-p2-strategy-analysis/SKILL.md` — existing-solutions scan now requires the **4-layer** model (direct / indirect / potential acquirers / adjacent movers), a **Competitor Pain Mining** table (top complaints from reviews + sources), and a **Steelman** paragraph. *(G4)*
- **T1.3** `recipes/p5-product-definition.yaml` — PRD must include **Non-goals** + an **evidence-gated Feature-add bar** ("real user signal or founder enthusiasm?") and confirm requirements trace to the **validated** problem, not the assumed one. *(G6, G11)*
- **T1.4** `recipes/p2` + `recipes/p4` — `$assumption-challenger` promoted from optional → **REQUIRED red-team / pre-mortem** before completing each phase; **Skeptic check** added to `templates/outcome-review.md`. *(G1, C5)*
- **T1.5** `templates/decision-memo.md` + `templates/outcome-review.md` — **Moat check** ("if a well-funded incumbent shipped this today, would users stay?"). *(G10)*

## Done — Tier 3.1: new P6 validation-prototype phase (clean renumber to P1–P10)

The pipeline is now **10 phases**. New **P6 = Validation Prototype** (single core interaction → ~5 target users → go/pivot/waive; **non-gated and waivable** with a recorded rationale, per your "no hard floor" decision). Old phases shifted: Architecture **P6→P7**, Feature-Spec **P7→P8**, Build **P8→P9**, Outcome **P9→P10**. Gates moved with them: Architecture Gate now at **P7**, Release Gate at **P9** (Strategy@P3, Product@P5 unchanged).

Changed (canonical + both synced mirrors, 145 paths total):
- **Engine** — `pipeline.py` (`PHASES` +P10, `GATE_PHASES`, `blocked_next`, complete-time gate map, valid-phase messages, speckit P7→P8); `pipeline_gate.py` (`GATE_NEXT_PHASES`: architecture→P8, release→P10).
- **Recipes** — `git mv` p6→p7…p9→p10 + internal `phase:`/`complete` renumber; **new** `p6-validation-prototype.yaml` (`$assumption-challenger` + concierge/fake-door tests, waiver step).
- **Entry skills** — `git mv` 4 dirs + renumbered content; **new** `idea2product-p6-validation-prototype/` (SKILL.md + openai.yaml); **new** `templates/validation-prototype.md`.
- **State/config** — `pipeline-state.yaml` (+P10), `pipeline-config.yaml` (new p6 estimate, gates after P7/P9).
- **P0 + scripts + docs** — guided-flow, pipeline-map, rollback, install.py (16 skills), check_skill_refs, README ×2 (10-phase table + diagram), PACKAGE-CONTENTS, TECHNICAL-DEEP-DIVE, adapter guides (common/opencode/claude-code/AGENT-ADAPTERS/PIPELINE-USER-GUIDE), develop-adr note.

**Verified:** `py_compile` OK · `check_skill_refs` resolves all 10 recipes · `doctor` healthy · `run P5/P6/P7/P9` print correct gates (P5 product, P6 none, P7 architecture, P9 release) · gate-unblock transitions all correct (strategy→P4, product→P6, architecture→P8, release→P10) · sync clean.

## Done — Phase A & B (Occam plan, verified)

- **A1 (flagship):** assumption-register provenance fields + `parse_register` + `doctor` & `gate request` **non-blocking** confirmation-bias warnings (closed-without-user-contact / zero-disconfirming / register asymmetry). Unit-tested: clean register quiet, crafted register fires all 3.
- **A2:** PMF instruments (Sean Ellis 40% / effort / three R's) + false-PMF caution in `outcome-review.md` and `validation-prototype.md`.
- **A3:** `templates/interview-plan.md` (who+where, bias-audited past-behavior questions, debrief, every-5 asymmetry), wired into P4 recipe (recommended; reuses `$discover-interview-synthesis`). **No new skill** (Occam).
- **A4 (minimal):** `gate request` surfaces the bias-watch at the human decision point (reuses A1).
- **B:** `CHANGELOG.md` (official record); P10 recipe reminds to record assumption provenance.
- **Verified:** compile OK · check_skill_refs 10 recipes OK · doctor healthy · sync clean.

See playbook-fidelity audit: [07-playbook-fidelity-audit.md](07-playbook-fidelity-audit.md).
