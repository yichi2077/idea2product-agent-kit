# pipeline-gate

Request gates and explain manual approval requirements. This skill cannot approve gates.

## Rules

- Implicit invocation is disabled.
- Use only when a recipe explicitly lists `$pipeline-gate`.
- Record outputs in the configured pipeline files.
