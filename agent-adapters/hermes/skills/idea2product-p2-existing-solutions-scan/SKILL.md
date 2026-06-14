---
name: idea2product-p2-existing-solutions-scan
description: "Before full P2 strategy analysis, search for existing products, services, open-source projects, and substitute workflows that may already solve the expanded idea; require a user decision before continuing."
---

# idea2product-P2-existing-solutions-scan

Use this at the start of P2, after P1 has produced a real
`docs/00-idea/idea-brief.md` and before committing to deeper strategy/product work.
The purpose is to protect the user from building something they should simply use,
buy, partner with, or learn from.

## Required Workspace

Work from the target project root. If `.pipeline/scripts/pipeline.py` is missing,
initialize the workspace first by invoking `$idea2product-p0-guided-flow`, then run P2.

## Inputs

- `docs/00-idea/idea-brief.md`
- `.pipeline/state/assumption-register.yaml`
- `.pipeline/state/risk-register.yaml`

If the idea brief is missing, still scaffolded, or too thin to generate useful
queries, stop and ask the user to clarify the idea through P1. Do not invent a
product category.

## Search

Use web search from the agent runtime. Search for:

- direct competitors
- indirect competitors
- substitute workflows
- open-source projects
- SaaS, apps, services, templates, and no-code tools that are ready to use

Generate queries from the idea brief's user, job-to-be-done, problem, core
capability, constraints, and target market. Do not rely on one generic query.

## Output

Write `docs/10-strategy/existing-solutions-scan.md` with this exact structure:

```md
# Existing Solutions Scan

## Source Idea
[summary of the idea from docs/00-idea/idea-brief.md]

## Search Timestamp
[ISO timestamp]

## Search Queries
- [query 1]
- [query 2]

## Candidate Solutions
| Name | URL | Type | Ready to Use | Fit | Gaps | Notes |
| --- | --- | --- | --- | --- | --- | --- |

## Classification
[perfect_match | good_enough | partial_match | reference_only | no_credible_solution_found | search_unavailable]

## Recommendation
[use_existing | buy | partner | build_differentiated | continue_research | retire_recommended]

## User Decision
[pending | use_existing | buy | partner | build_differentiated | continue_build | continue_research | retire]

## Rationale
[why the recommendation and user decision are reasonable, tied to the candidate evidence]
```

## User Decision

If the scan finds a `perfect_match` or `good_enough` solution, stop before deeper P2
work and tell the user:

- what existing solution appears usable now
- which parts of the idea it covers
- what gaps remain
- whether the best next step is use existing, buy, partner, build a differentiated
  wedge, continue research, or retire

Then ask for the user's decision and write it into `## User Decision`. Leave it as
`pending` only while waiting for the user. `stage complete P2` rejects `pending`.

If search is unavailable, use `Classification: search_unavailable`, explain the
access limitation in `## Rationale`, and record the market/solution uncertainty as
an assumption or risk in the registers before continuing.

## Never

- Never auto-retire the project. Use `$idea2product-p0-retire` only after explicit
  user confirmation.
- Never continue as if no alternatives exist when search failed.
- Never treat an existing product as automatic proof the idea is bad; identify the
  possible differentiated wedge if the user wants to keep building.
