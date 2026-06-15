# Pipeline Host Wiring

The system entrypoint is the `pipeline` command implemented by `.pipeline/scripts/pipeline.py`.

Daily commands:

- `python3 .pipeline/scripts/pipeline.py status` on macOS/Linux; `python .pipeline/scripts/pipeline.py status` on Windows
- `python3 .pipeline/scripts/pipeline.py next` on macOS/Linux; `python .pipeline/scripts/pipeline.py next` on Windows
- `python3 .pipeline/scripts/pipeline.py resume` on macOS/Linux; `python .pipeline/scripts/pipeline.py resume` on Windows
- `python3 .pipeline/scripts/pipeline.py run P1` on macOS/Linux; `python .pipeline/scripts/pipeline.py run P1` on Windows
- `python3 .pipeline/scripts/pipeline.py gate request strategy` on macOS/Linux; `python .pipeline/scripts/pipeline.py gate request strategy` on Windows
- `python3 .pipeline/scripts/pipeline.py assumptions due` on macOS/Linux; `python .pipeline/scripts/pipeline.py assumptions due` on Windows

Rules for agents:

- Before phase work, run `pipeline run Px` and follow the recipe skill list.
- Recipes are closed lists; do not invoke skills outside the current recipe.
- Vendored skills are excerpts from larger upstream collections, kept verbatim. Their text
  may cross-reference sibling skills (e.g. `superpowers:…`, `foundation-…`) that are not
  bundled here. Such a reference is informational: if the named skill is not in
  `.pipeline/vendor/` or the current recipe, do not block on it and do not try to install
  it — the recipe is authoritative for what to run.
- Gates are human-owned. In the default **light** gate mode the agent may RECORD a human's verdict
  (`pipeline_gate.py approve|reject <gate> --rationale "..."`) but ONLY after the human explicitly
  approves or rejects in the conversation — never autonomously, never with an invented rationale. In
  **strict** mode the agent cannot approve at all (the human uses a separate terminal + challenge
  code). Check the mode with `pipeline.py gate mode`.
- Do not edit gate approval fields directly in `.pipeline/state/pipeline-state.yaml`.
- Stay in the chat — the user should never be sent to a terminal. If the engine prints an install
  command for a missing tool (e.g. Spec Kit, `uv`), YOU run that exact command yourself and report it
  done. Never tell the user to open a terminal and run it.
- Version control is your job, not the user's. Before `stage complete Px`, commit that phase's
  artifacts for them: `git add docs .pipeline && git commit -m "idea2product: complete Px (<phase>)"`
  (run `git init` once first if the folder is not yet a git repo). Never `git push`. This keeps gate
  approval tags and resume points meaningful.
- All pipeline skills must keep `agents/openai.yaml` with `allow_implicit_invocation: false`.

User-level entry skills include `$idea2product-p0-guided-flow`, `$idea2product-p0-status`, `$idea2product-p0-resume`, `$idea2product-p0-rollback`, `$idea2product-p0-doctor`, `$idea2product-p0-retire`, and `$idea2product-p1-idea-expansion` through `$idea2product-p9-outcome-review`. P2 strategy analysis includes the existing-solutions scan as a required first step.
