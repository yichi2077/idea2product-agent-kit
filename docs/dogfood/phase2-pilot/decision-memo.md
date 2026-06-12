# Decision Memo: Commit to Phase2 Feedback Loop Hardening

## Decision

COMMIT to implementing the closed-loop hardening increment on a feature branch before adding data connectors or slide generation.

## Rationale

The repo already contains interview synthesis, experiment result, market research, and PM critic capabilities. The missing product capability is enforcement and feedback: downstream findings must be able to reopen upstream phases, completed artifacts must be monitored for drift, and gates must require the evidence artifacts they claim to depend on.

## Scope

In scope: reopen command, phase metadata hashes, stale warnings, product/strategy gate preconditions, state invariant validation, mirror sync, and dogfood P1-P3 evidence.

Out of scope: GA/DB connectors, crawler integrations, deck renderer, and automated agent approval.

## Gate Ask

Request Strategy Gate after P3 completion with this decision memo and the strategy red-team report present.
