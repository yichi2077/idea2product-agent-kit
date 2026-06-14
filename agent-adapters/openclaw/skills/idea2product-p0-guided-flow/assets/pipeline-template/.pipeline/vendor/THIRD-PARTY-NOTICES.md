# Third-Party Notices — Vendored Skills

The pipeline bundles 34 third-party skills plus 2 first-party custom skills. Every
vendored skill carries its upstream `LICENSE` and a `SOURCE.yaml` recording its origin
and commit. All licenses are permissive (MIT / Apache-2.0) and compatible with this
kit's MIT license. This file is the at-a-glance manifest; the per-skill `LICENSE` and
`SOURCE.yaml` files remain authoritative.

## Upstream sources

| Source (short name) | Upstream repository | License | Skills |
|---------------------|---------------------|---------|--------|
| `claude-skills` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | MIT | 5 strategy |
| `pm-skills` | [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) | Apache-2.0 | 22 product |
| `superpowers` | [obra/superpowers](https://github.com/obra/superpowers) | MIT | 7 engineering |
| `local` | first-party (this repository) | MIT (root LICENSE) | 2 custom |

> Apache-2.0 (the `pm-skills` set) requires that this NOTICE and the per-skill `LICENSE`
> copies travel with redistribution — they do, inside `.pipeline/vendor/`.

## Skill inventory

### Strategy — `alirezarezvani/claude-skills` @ `4a3c05b` (MIT)
- assumption-challenger · business-investment-advisor · ceo-advisor · financial-analyst · market-research

### Product — `product-on-purpose/pm-skills` @ `f82e5d2` (Apache-2.0)
- define-hypothesis · define-jtbd-canvas · define-opportunity-tree · define-prioritization-framework · define-problem-statement
- deliver-acceptance-criteria · deliver-edge-cases · deliver-launch-checklist · deliver-prd · deliver-user-stories
- develop-adr · develop-design-rationale · develop-solution-brief · develop-spike-summary
- discover-interview-synthesis · foundation-lean-canvas · iterate-lessons-log · iterate-pivot-decision
- measure-experiment-design · measure-experiment-results · measure-instrumentation-spec · utility-pm-critic

### Engineering — `obra/superpowers` @ `6fd4507` (MIT)
- executing-plans · finishing-a-development-branch · receiving-code-review · requesting-code-review
- systematic-debugging · test-driven-development · verification-before-completion

### Custom (first-party, MIT) — `local`
- pipeline-gate · prd-to-speckit-handoff

## Vendoring policy (why these, and what was rejected)

Skills are kept as coherent per-source sets: the engineering set cross-references itself
by name (e.g. `executing-plans` → `finishing-a-development-branch`), and the product set
shares one upstream's structure and metadata. Replacing one skill with a different repo's
version would break those references and mix licenses, so swaps must clear a high bar:
**verified higher quality AND license-compatible AND coherent with the existing set.**

A 2026-06 review of proposed alternatives found none that cleared the bar:

| Candidate source | License | Decision | Reason |
|------------------|---------|----------|--------|
| Candidate (target skill) | License (verified) | Decision | Evidence |
|--------------------------|--------------------|----------|----------|
| deanpeters/Product-Manager-Skills | **CC BY-NC-SA 4.0** | rejected | NonCommercial + ShareAlike — would force the kit under BY-NC-SA |
| slgoodrich/agents — market-sizing (→ market-research) | **PolyForm Noncommercial 1.0** | rejected | NonCommercial; prompt-only; `market-research` already has TAM/SAM/SOM scripts |
| Mathews-Tom/armory — market-analyzer (→ market-research) | MIT | rejected | Prompt-only, "less rigorous computationally" than our 6-script `market-research`; `idea-validator` overlaps the pipeline's own orchestration |
| alirezarezvani/claude-cto-team — assumption-challenger | MIT | rejected | Prompt-only, "less comprehensive"; execution-framing (timeline/resource) fits the idea→strategy nodes worse than our DVF mapping + `assumption_mapper.py` |
| phuryn/pm-skills — lessons-learned (→ iterate-lessons-log) | MIT | rejected | No lessons-log exists — only sprint `retro` (no decay/classification); discovery/red-team overlap skills that already ship scripts |
| me2resh/agent-decision-record (→ develop-adr) | CC BY 4.0 | rejected (swap) | Novel agent/model/trigger idea, but it is a CC-BY command + git-hooks bundle, not a SKILL.md; mixes a third license and breaks pm-skills coherence (idea may be added in-house later) |
| wondelai/skills — mom-test (→ discover-interview-synthesis) | book fair-use | rejected | Interview *technique* (input layer) — complement, not a substitute for interview *synthesis* |
| awesome-skills/code-review-skill (→ requesting/receiving-code-review) | MIT | rejected (swap) | Language-specific review ruleset (16k lines, 20+ langs) — complements, does not replace, the superpowers review *workflow*; swap breaks the request/receive pairing |
| coreyhaines31/marketingskills — ab-testing (→ measure-experiment-*) | MIT | rejected | Unified marketing-growth skill, different domain framing; not superior to the product-experiment `measure-*` set; breaks pm-skills coherence |
| poteto/noodle — adversarial-review (→ utility-pm-critic) | n/a | rejected | Skill does not exist (misattribution); `utility-pm-critic` already returns P0–P3 findings |
| alirezarezvani/claude-skills — cs-ceo-advisor (→ ceo-advisor) | MIT | rejected | "cs-ceo-advisor" does not exist; HEAD `ceo-advisor` (v2.0.0, 2026-03-05) is not newer than our snapshot and ships the same 2 scripts |

Freshness was verified, not assumed: pm-skills CHANGELOG shows no skill file changed after the
2026-06-12 vendor snapshot (latest release 2.26.0 / 2026-06-10; catalog frozen at 65 — the "v2.9.x"
figure is the separate `pm-skills-mcp` server's version, not the file repo); `obra/superpowers` HEAD
matches the vendored engineering copies; `claude-skills` HEAD `ceo-advisor` is not newer than ours.

Re-vendoring **newer versions from the existing sources** is always welcome when upstream
materially improves a skill (record the new commit in its `SOURCE.yaml`).
