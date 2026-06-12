# Pipeline Host Wiring

The system entrypoint is the `pipeline` command implemented by `.pipeline/scripts/pipeline.py`.

Daily commands:

- `python .pipeline/scripts/pipeline.py status`
- `python .pipeline/scripts/pipeline.py next`
- `python .pipeline/scripts/pipeline.py resume`
- `python .pipeline/scripts/pipeline.py run P1`
- `python .pipeline/scripts/pipeline.py gate request strategy`
- `python .pipeline/scripts/pipeline.py assumptions due`

Rules for agents:

- Before phase work, run `pipeline run Px` and follow the recipe skill list.
- Recipes are closed lists; do not invoke skills outside the current recipe.
- Gate approval is not available to agents.
- Do not edit gate approval fields directly in `.pipeline/state/pipeline-state.yaml`.
- All pipeline skills must keep `agents/openai.yaml` with `allow_implicit_invocation: false`.

User-level entry skills include `$idea2product-p0-guided-flow`, `$idea2product-p0-status`, `$idea2product-p0-resume`, and `$idea2product-p1-idea-expansion` through `$idea2product-p9-outcome-review`.
