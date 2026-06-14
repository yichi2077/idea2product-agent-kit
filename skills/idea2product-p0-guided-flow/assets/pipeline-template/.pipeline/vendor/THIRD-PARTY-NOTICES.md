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
| deanpeters/Product-Manager-Skills | CC BY-NC-SA | rejected | NonCommercial — incompatible with MIT redistribution |
| me2resh/agent-decision-record | CC BY 4.0 | rejected | Attribution-required; marginal gain over Apache `develop-adr`; mixes a third license |
| phuryn/pm-skills | MIT | rejected | Prompt-only; overlaps `assumption-challenger` / `define-prioritization-framework` / `utility-pm-critic`, which already ship scoring scripts |
| Mathews-Tom/armory | MIT | rejected | No evidence of exceeding our script-backed skills; cross-set swap breaks coherence |
| awesome-skills/code-review-skill | MIT | rejected | Different kind (language linting), complements rather than replaces the superpowers review workflow |

Re-vendoring **newer versions from the existing sources** is always welcome when upstream
materially improves a skill (record the new commit in its `SOURCE.yaml`).
