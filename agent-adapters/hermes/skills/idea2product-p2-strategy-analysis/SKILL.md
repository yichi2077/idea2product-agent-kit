---
name: idea2product-p2-strategy-analysis
description: "Analyze the approved idea as a strategy problem, starting with an existing-solutions scan so the user can use, buy, partner, retire, or deliberately build a differentiated product before deeper strategy work. Use when the user explicitly asks for idea2product-P2-strategy-analysis, P2, phase 2, or this step of the idea-to-product pipeline."
---

# idea2product-P2-strategy-analysis

Analyze the approved idea as a strategy problem. Start by checking whether an
existing product, service, open-source project, or substitute workflow already solves
the idea well enough that the user should use, buy, partner, or retire instead of
building. Only then continue into issue tree, hypothesis tree, market, competition,
trend, right to win, unit economics, strategic options, evidence quality, and unknowns.

## Required Workspace

Work from the target project root when possible. If `.pipeline/scripts/pipeline.py` is missing, initialize the workspace first by invoking `idea2product-p0-guided-flow`, then run P2.

## Run

From the workspace root, run:

```bash
python3 .pipeline/scripts/pipeline.py run P2
```

On Windows, use:

```powershell
python .pipeline/scripts/pipeline.py run P2
```


Then follow the printed recipe exactly. The recipe separates required skills, conditional skills, optional skills, external tools, non-skill process steps, outputs, and completion commands for this phase.

## Main Output

`docs/10-strategy/existing-solutions-scan.md`

`docs/10-strategy/strategy-research-note.md`

## Existing Solutions Scan

This scan is a required first step inside P2. Use it after P1 has produced a real
`docs/00-idea/idea-brief.md` and before committing to deeper strategy/product work.
The purpose is to protect the user from building something they should simply use,
buy, partner with, or learn from.

### Inputs

- `docs/00-idea/idea-brief.md`
- `.pipeline/state/assumption-register.yaml`
- `.pipeline/state/risk-register.yaml`

If the idea brief is missing, still scaffolded, or too thin to generate useful
queries, stop and ask the user to clarify the idea through P1. Do not invent a
product category.

### Search

Use web search from the agent runtime. Cover four competitor layers (the fix for
"competitor blindness" — do not only look at direct rivals):

- Layer 1 — direct competitors (do almost the same thing)
- Layer 2 — indirect competitors / substitute workflows (solve the same job differently)
- Layer 3 — potential acquirers / incumbents with an adjacent capability who could enter
- Layer 4 — adjacent movers (not in this space today, but a plausible next step away)

Include open-source projects and ready-to-use SaaS, apps, services, templates, and
no-code tools at every layer.

Generate queries from the idea brief's user, job-to-be-done, problem, core
capability, constraints, and target market. Do not rely on one generic query.

### Output

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
| Name | URL | Layer (1-4) | Type | Ready to Use | Fit | Gaps | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Competitor Pain Mining
[Free qualitative research: from reviews (App Store / G2 / Reddit / forums), the top
recurring complaints about the leading alternatives. Cite sources.]
| Competitor | Top recurring pain | Source | Does our hypothesis address it? |
| --- | --- | --- | --- |

## Steelman (strongest rival)
[The most persuasive case for why the strongest competitor WINS and we fail. Is our
differentiation an actual moat, or a feature they can copy in a quarter?]

## Classification
[perfect_match | good_enough | partial_match | reference_only | no_credible_solution_found | search_unavailable]

## Recommendation
[use_existing | buy | partner | build_differentiated | continue_research | retire_recommended]

## User Decision
[pending | use_existing | buy | partner | build_differentiated | continue_build | continue_research | retire]

## Rationale
[why the recommendation and user decision are reasonable, tied to the candidate evidence]
```

### User Decision

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

## Rules

- Do not skip earlier gates or approved dependencies.
- Do not invent a fake business idea for P1-P3 validation.
- Perform the existing-solutions scan yourself first. If the scan finds a ready
  existing solution, stop and get the user's decision before continuing into deeper
  market, competition, strategy, or product analysis.
- Do not complete P2 while `existing-solutions-scan.md` has `User Decision: pending`
  or says the user chose `use_existing` / `retire`.
- Never auto-retire the project. Use `$idea2product-p0-retire` only after explicit
  user confirmation.
- Never continue as if no alternatives exist when search failed.
- Never treat an existing product as automatic proof the idea is bad; identify the
  possible differentiated wedge if the user wants to keep building.
- If the command reports a blocker, report the blocker and the concrete missing input.
- After editing pipeline state, re-run `python3 .pipeline/scripts/pipeline.py status` (or `python` on Windows) to confirm the workspace is consistent.
