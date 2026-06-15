# Technical Deep Dive & Operational Manual

This document contains the detailed operational instructions and architectural breakdown for the `idea2product-agent-kit`. It is intended for developers, agent configurators, and advanced users who want to look under the hood.

---

## 1. Installation Details (Per-Agent)

> **Note:** Use `python3` on macOS/Linux. On Windows, use `python` instead.

### Claude Code
```bash
python3 scripts/install.py skills --target claude-code
python3 scripts/install.py adapters /path/to/your-project --agent claude-code
```
Installs skills to `~/.claude/skills` and generates a `CLAUDE.md` in your project root.

### Codex (OpenAI)
```bash
python3 scripts/install.py skills --target codex
python3 scripts/install.py adapters /path/to/your-project --agent codex
```
Installs skills to `~/.agents/skills`. Each skill gets an `openai.yaml` config. Generates a `README.md` with agent instructions in your project.

### Cursor
```bash
python3 scripts/install.py adapters /path/to/your-project --agent cursor
```
Generates `README.md` + `.cursor/rules` for Cursor's rule system.

### OpenCode
```bash
python3 scripts/install.py adapters /path/to/your-project --agent opencode
```
Generates an `AGENTS.md` in your project root.

### Hermes
```bash
python3 scripts/install.py adapters /path/to/your-project --agent hermes
```
Generates `AGENTS.hermes.md` in your project root. To also mirror skills to `~/.hermes/skills/`:
```bash
python3 scripts/install.py adapters /path/to/your-project --agent hermes --install-user-skills
```

### OpenClaw
```bash
python3 scripts/install.py adapters /path/to/your-project --agent openclaw
```
Generates `AGENTS.openclaw.md`, `SOUL.md`, `TOOLS.md`, and copies skills to your project.

### Generic (Any Agent)
```bash
python3 scripts/install.py adapters /path/to/your-project --agent generic
```
Generates a universal `AGENTS.generic.md` that works with any agent supporting markdown-based instructions.

---

## 2. Scaffold and Upgrade

### Scaffold a New Project manually
```bash
python3 scripts/install.py scaffold /path/to/new-project
```
Creates the full `.pipeline/` directory structure with state files, templates, and recipes in your target repo.

### Upgrade an Existing Project
When the kit improves, update an already-scaffolded project's engine without losing your work:
```bash
python3 scripts/install.py upgrade /path/to/my-project
```
Replaces the engine machinery (`scripts/`, `recipes/`, `vendor/`, `custom-skills/`, `templates/`) and **preserves your `state/`, `reports/`, and `docs/`** untouched. The files it replaces are backed up in place as `*.bak-<timestamp>` (delete once verified). Run `python3 .pipeline/scripts/pipeline.py doctor` afterward to confirm consistency.

---

## 3. Spec Kit (optional)

Phase **P7** produces a *Specify Packet* and hands it to [Spec Kit](https://github.com/github/spec-kit) — GitHub's spec-driven-development toolkit — via its `speckit.*` commands (`speckit.specify`, `speckit.plan`, `speckit.tasks`, …). **Spec Kit is an optional external dependency maintained separately by GitHub.** The pipeline always produces the packet; you need Spec Kit only to run the spec-driven implementation loop on it.

Check status or install it with the bundled helper:
```bash
python3 scripts/install.py speckit            # show whether Spec Kit is installed + the exact install commands
python3 scripts/install.py speckit --install  # run the per-project init for you (requires uv)
```

Or install it directly (requires [uv](https://docs.astral.sh/uv/)):
```bash
# one-off, per project (run inside your project dir):
uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai claude
# or install the CLI persistently:
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```
`pipeline.py run P7` and `pipeline.py doctor` print a non-blocking reminder (with the install command) when Spec Kit is not detected.

---

## 4. Utility Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| **Status** | `status` | Show current phase, progress, pending gates, due assumptions |
| **Resume** | `resume` | Resume a paused or interrupted pipeline from saved state |
| **Rollback** | `rollback` | Roll back to a previous phase (reopens it, preserves history) |
| **Doctor** | `doctor` | Diagnose pipeline health — check state files, missing artifacts, broken references |
| **Retire** | `retire --reason "..."` | Gracefully retire a pipeline with a documented reason |
| **Handoff** | `handoff` | Generate a context document for handing the project to another agent or person |

### Other Useful Commands
```bash
run p4              # Run a specific phase
stage complete p4   # Manually mark a phase complete
reopen p3 --reason "New market data"  # Reopen a completed phase
assumptions due     # List assumptions that need validation
```

---

## 5. Architecture Details

### What's in the Box
```
idea2product-agent-kit/
├── scripts/
│   ├── install.py             # Main installer (skills, adapters, scaffold)
│   └── *.ps1                  # Windows convenience wrappers
│
├── skills/                    # 15 pipeline skills
│   ├── p0-guided-flow/        # End-to-end guided walkthrough
│   ├── p0-status/             # Pipeline status
│   ├── p1-idea-brief/         # Phase 1: Idea capture
│   └── ... (p2 through p9)
│
├── pipeline-template/         # Scaffolded into target repo as .pipeline/
│   ├── .pipeline/
│   │   ├── scripts/
│   │   │   ├── pipeline.py        # Pipeline engine — phase execution, state management
│   │   │   ├── pipeline_gate.py   # Gate approval — challenge/response system
│   │   │   ├── link_skills.py     # Link skills into agent skill directories
│   │   │   └── review_due.py      # Check for due reviews and assumptions
│   │   ├── state/                 # Pipeline state files
│   │   ├── templates/             # 10 document templates
│   │   ├── recipes/               # 9 phase recipes (YAML)
│   │   └── vendor/                # Vendored domain skills
│
└── agent-adapters/            # Per-agent configuration generators
```

### How It Works
1. **Recipes** (`.pipeline/recipes/p*.yaml`) define each phase — what steps to run, which templates to use, which vendor skills to invoke
2. **Skills** (`skills/p*`) contain the agent instructions (`SKILL.md`) and agent-specific configs (`agents/` directory)
3. **Vendor skills** (`.pipeline/vendor/`) are domain-expert skills the pipeline invokes — strategy analysis, product documentation, engineering practices
4. **State files** (`.pipeline/state/`) track progress, assumptions, risks, and decisions across sessions
5. **Adapters** generate the right instruction files for your agent so it knows how to run the pipeline
6. **Scripts** handle state transitions, gate approvals, and maintenance tasks

### Maintainer integrity checks

Two stdlib-only checks keep the kit internally consistent — run both before opening a PR:

```bash
python3 scripts/sync_bundled_copies.py --check   # the 4 bundled copies match their canonical source
python3 scripts/check_skill_refs.py --check      # every recipe $skill resolves to a bundled skill
```

`check_skill_refs.py` with no flag also prints an informational report of cross-references in
vendored skill bodies that point at sibling skills not bundled here. Those are expected —
vendored skills are verbatim excerpts and execution is recipe-driven (see
`.pipeline/vendor/THIRD-PARTY-NOTICES.md`); the report just makes the surface visible, so a
new, unintended reference is easy to spot.

---

## 6. FAQ

### Do I need all 15 skills installed?
No. Install only the phases you need. The pipeline is sequential but each phase works independently once prerequisites are met.

### Can I skip phases?
You can, but gates enforce minimum completeness. For example, you can't reach P4 (Product Discovery) without passing the Strategy Gate after P3.

### What if I want to go back to an earlier phase?
Use `reopen p3 --reason "New information"` or `rollback`. Previous work is preserved in the decision log — nothing is lost.

### Does this work without an internet connection?
Yes. The kit uses only Python stdlib and Git. Domain skills and templates are all local files. The agent may need internet for its own API calls, but the pipeline infrastructure is fully offline.

### Can I use this with multiple agents on the same project?
Yes. Run `python3 scripts/install.py adapters /path/to/your-project` with different `--agent` targets. Each adapter generates its own instruction files without overwriting others.

### What happens if my agent session dies mid-phase?
Use `resume` to pick up where you left off. Pipeline state is saved to `.pipeline/state/` after every meaningful step. You can also run `doctor` to check for any inconsistencies.

### How do I approve a gate in strict mode?
If you want a harder guarantee that the agent *cannot* approve at all, switch to **strict** mode (`python3 .pipeline/scripts/pipeline.py gate mode strict`): approval then happens only in a separate real terminal with a random challenge code. (By default, you are in **light** mode, where you just approve via chat).

### Can I customize the templates?
Absolutely. Templates in `.pipeline/templates/` are plain markdown. Edit them to match your workflow. Recipes reference templates by name, so your customizations are picked up automatically.

### How does the anti-confirmation bias work?
P3 (Strategy Decision) forces the agent to compare all viable options — build, buy, partner, and do-nothing — rather than just justifying a pre-made decision. A cross-model red-team review (using `red-team-strategy.md`) challenges the reasoning before you reach the Strategy Gate.
