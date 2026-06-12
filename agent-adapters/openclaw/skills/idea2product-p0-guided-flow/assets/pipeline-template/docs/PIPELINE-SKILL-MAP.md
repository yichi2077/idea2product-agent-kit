# Pipeline Skill Map

Generated: 2026-06-12

This map records the closed recipe behind each explicit `idea2product-Px-*` entry skill. Recipes separate required skills from conditional or optional skills so phase entry skills do not recursively call orchestration skills or run evidence-dependent skills before their inputs exist.

## Source Families

- Strategic skills: vendored from `alirezarezvani/claude-skills` style strategy/business advisory prompts.
- Product skills: vendored from `product-on-purpose/pm-skills`, with local names preserving the upstream skill intent and adding domain prefixes such as `define-`, `deliver-`, `develop-`, `measure-`, `utility-`, and `iterate-`.
- Engineering skills: vendored from `obra/superpowers`.
- Local pipeline skills: created for this pipeline where the plan requires orchestration, gates, or Spec Kit handoff behavior not provided by upstream prompt packs.

## Phase Recipes

| Phase | Entry skill | Required recipe skills | Conditional or optional skills | Notes |
| --- | --- | --- | --- | --- |
| P1 | `idea2product-p1-idea-expansion` | `$assumption-challenger` | None | Expands and stress-tests the raw idea before strategy work. |
| P2 | `idea2product-p2-strategy-analysis` | `$market-research`, `$business-investment-advisor` | `$financial-analyst` only with real revenue/cost/cash-flow/budget/forecast data; `$assumption-challenger` as optional strategy review | Avoids forcing finance-analysis workflows onto early rough ideas. |
| P3 | `idea2product-p3-strategy-decision` | `$ceo-advisor` | `$assumption-challenger` optional for final pre-mortem or cross-model red-team | Strategy Gate is requested with `pipeline gate request strategy`, not as a recipe skill. |
| P4 | `idea2product-p4-product-discovery` | `$foundation-lean-canvas`, `$define-problem-statement`, `$define-jtbd-canvas`, `$define-opportunity-tree`, `$define-hypothesis`, `$define-prioritization-framework`, `$develop-solution-brief` | `$discover-interview-synthesis` with raw interviews; `$measure-experiment-design` when designing validation; `$measure-experiment-results` only after real data; `$iterate-pivot-decision` when evidence requires it | Uses Product on Purpose discovery order and keeps validation-result skills evidence-gated. |
| P5 | `idea2product-p5-product-definition` | `$deliver-prd`, `$deliver-user-stories`, `$deliver-acceptance-criteria`, `$deliver-edge-cases`, `$measure-instrumentation-spec`, `$utility-pm-critic` | None | Product Gate is requested with `pipeline gate request product`. Run `$utility-pm-critic` in a fresh context against the completed PRD. |
| P6 | `idea2product-p6-architecture-handoff` | `$prd-to-speckit-handoff`, `$develop-adr`, `$develop-design-rationale` | `$develop-spike-summary` only after a real technical spike; Context7 CLI as external tool | Architecture Gate is requested with `pipeline gate request architecture`; spike summaries are not generated before spike evidence exists. |
| P7 | `idea2product-p7-feature-specification` | External Spec Kit command chain | `$prd-to-speckit-handoff` only when packets are missing/stale, PRD was re-approved, or traceability fails | Default path consumes the approved Specify Packet and runs `speckit.specify`, `speckit.clarify`, `speckit.checklist`, `speckit.plan`, `speckit.tasks`, `speckit.analyze`. |
| P8 | `idea2product-p8-build-release` | `$executing-plans`, `$test-driven-development`, `$verification-before-completion`, `$requesting-code-review`, `$receiving-code-review`, `$deliver-launch-checklist`, `$finishing-a-development-branch` | `$systematic-debugging` only when tests fail, a bug appears, or behavior differs from expectation | Release Gate is requested with `pipeline gate request release`; debugging is not a mandatory happy-path skill. |
| P9 | `idea2product-p9-outcome-review` | `$measure-experiment-results`, `$iterate-pivot-decision`, `$iterate-lessons-log` | `$assumption-challenger` optional after outcomes and lessons are recorded | Normalizes real outcomes first, then makes pivot/persevere decisions and records durable lessons. |

## Orchestration Boundary

`$pipeline-gate` is not a domain skill and is not part of any P1-P9 recipe's required or conditional skill list. Gate behavior is handled by pipeline commands such as:

```powershell
python .pipeline/scripts/pipeline.py stage complete P5
python .pipeline/scripts/pipeline.py gate request product
```

This keeps phase entry skills thin:

1. Run `pipeline run Px`.
2. Follow the phase recipe.
3. Produce and verify artifacts.
4. Run the listed `completion_commands`.

## Validation

The command below validates recipe YAML, required recipe fields, `post_skill_verification`, phase coverage, duplicate phases, required/conditional/optional skill references, and that every `$skill` exists under `.agents/skills/<skill>/SKILL.md`.

```powershell
python .pipeline/scripts/validate_recipes.py
```

It is also part of both verification entrypoints:

```powershell
powershell -ExecutionPolicy Bypass -File .pipeline/scripts/verify.ps1
sh .pipeline/scripts/verify.sh
```
