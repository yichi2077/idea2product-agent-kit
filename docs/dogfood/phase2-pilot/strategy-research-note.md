# Strategy Research Note: Phase2 Feedback Loop Hardening

## Decision Context

The kit is differentiated by owning upstream idea-to-product work before Spec Kit-style implementation planning. The main risk is not lack of more skills; it is that existing artifacts and reviews are not wired into an enforceable loop.

## Evidence Used

- Repo audit of pipeline commands showed no reopen/rework command before this increment.
- Recipe audit showed P5 already requires utility-pm-critic, but gate request did not verify the artifact.
- P4/P9 already include interview and experiment result skills, so new analytics connectors are premature.
- Template validation and mirror sync passed before the dogfood run.

## Strategic Options

1. Add external analytics connectors first: deferred because it expands surface area without proving workflow need.
2. Add deck/storytelling first: useful, but does not reduce spec drift.
3. Add closed-loop state mechanics first: selected because it directly addresses the highest-risk failure mode and improves all downstream work.

## Recommendation

Commit to a Phase2 increment focused on reopen, artifact staleness detection, gate preconditions, state invariants, and dogfood evidence.
