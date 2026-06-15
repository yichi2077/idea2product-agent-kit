# idea2product-agent-kit

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Agents](https://img.shields.io/badge/Agents-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20OpenCode%20%7C%20Hermes%20%7C%20OpenClaw%20%7C%20Generic-purple.svg)
![Version](https://img.shields.io/badge/Version-v1.1.0-orange.svg)

**A portable, agent-driven workflow that takes you from raw idea to shipped product — 9 phases, 4 human-only gates, zero guesswork.** Designed for solo operators wearing strategy, PM, and engineering hats simultaneously. Works with any coding agent you already use.

---

## Table of Contents

- [Pipeline Overview](#pipeline-overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Phase Reference](#phase-reference)
- [Gate System](#gate-system)
- [Utility Skills](#utility-skills)
- [Architecture](#architecture)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## Pipeline Overview

The pipeline follows three expand-contract funnels. Each phase expands evidence and options, then contracts into a decision or artifact:

```
 ══════════════════════════════════════════════════════════════════════
  idea2product-agent-kit v1.1.0 — 9 Phases · 4 Gates
 ══════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────────┐
  │                     FUNNEL 1: IDEA → STRATEGY                   │
  │             market / finance / risk evidence → decision          │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │   ┌─────┐        ┌─────┐        ┌─────┐                         │
  │   │ P1  │───────▶│ P2  │───────▶│ P3  │                         │
  │   │Idea │        │Stra-│        │Stra-│                         │
  │   │Brief│        │tegy │        │tegy │                         │
  │   │     │        │Rese-│        │Deci-│                         │
  │   │     │        │arch │        │sion │                         │
  │   └─────┘        └─────┘        └─────┘                         │
  │                                  ▼                               │
  │                           ╔═══════════╗                          │
  │                           ║  GATE 1   ║  ← STRATEGY GATE        │
  │                           ║ Strategy  ║    human approval        │
  │                           ╚═══════════╝                          │
  └──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                    FUNNEL 2: STRATEGY → PRODUCT                  │
  │                 options → defined product                        │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │   ┌─────┐        ┌─────┐        ┌─────┐                         │
  │   │ P4  │───────▶│ P5  │───────▶│ P6  │                         │
  │   │Prod-│        │Prod-│        │Archi│                         │
  │   │uct  │        │uct  │        │tec- │                         │
  │   │Disco│        │Defi-│        │ture │                         │
  │   │very │        │niti-│        │Hand-│                         │
  │   │     │        │on   │        │off  │                         │
  │   └─────┘        └─────┘        └─────┘                         │
  │              ▼                   ▼                               │
  │       ╔═══════════╗       ╔═══════════╗                          │
  │       ║  GATE 2   ║       ║  GATE 3   ║  ← human approval        │
  │       ║ Product   ║       ║Architectu ║                          │
  │       ║ after P5  ║       ║ after P6  ║                          │
  │       ╚═══════════╝       ╚═══════════╝                          │
  └──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                  FUNNEL 3: PRODUCT → DELIVERY                    │
  │              technical options → shipped product                 │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │   ┌─────┐        ┌─────┐        ┌─────┐                         │
  │   │ P7  │───────▶│ P8  │───────▶│ P9  │                         │
  │   │Fea- │        │Build│        │Out- │                         │
  │   │ture │        │  &  │        │come │                         │
  │   │Spec │        │Rele-│        │Revi-│                         │
  │   │     │        │ase  │        │ew   │                         │
  │   └─────┘        └─────┘        └─────┘                         │
  │                     ▼                                            │
  │              ╔═══════════╗                                       │
  │              ║  GATE 4   ║  ← RELEASE GATE (after P8)           │
  │              ║ Release   ║    human approval                     │
  │              ╚═══════════╝                                       │
  └──────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

- **Python 3.10+** (stdlib only — no pip packages required)
- **Git**
- A coding agent (one or more from the list below)
- **Spec Kit** — _optional_. Phase **P7** hands its Specify Packet off to [github/spec-kit](https://github.com/github/spec-kit)'s `speckit.*` commands for spec-driven delivery. The pipeline runs fine without it (P7 still produces the packet); installing it unlocks the full P7 → P8 flow. See [Spec Kit (optional)](#spec-kit-optional) below.

### Zero-Terminal Onboarding (recommended)

You don't have to run any commands yourself. Open your agent (Claude Code, Codex, Cursor…) in an **empty folder** and just say:

> *Initialize an idea2product project here.*

The agent clones the kit and runs the one-shot `init` for you — installing the skills, scaffolding the `.pipeline/` engine, and wiring the host adapter (auto-detected). One sentence, zero terminal typing. What the agent runs on your behalf:

```bash
git clone https://github.com/yichi2077/idea2product-agent-kit.git /tmp/idea2product-agent-kit
python3 /tmp/idea2product-agent-kit/scripts/install.py init .
```

Then tell it `run p1` to start. Prefer to set things up by hand? Use the per-agent steps below.

### Install for Your Agent

```bash
# Clone the repo
git clone https://github.com/yichi2077/idea2product-agent-kit.git
cd idea2product-agent-kit
```

> **Note:** Use `python3` on macOS/Linux. On Windows, use `python` instead.

#### Claude Code

```bash
python3 scripts/install.py skills --target claude-code
python3 scripts/install.py adapters /path/to/your-project --agent claude-code
```

Installs skills to `~/.claude/skills` and generates a `CLAUDE.md` in your project root.

#### Codex (OpenAI)

```bash
python3 scripts/install.py skills --target codex
python3 scripts/install.py adapters /path/to/your-project --agent codex
```

Installs skills to `~/.agents/skills`. Each skill gets an `openai.yaml` config. Generates a `README.md` with agent instructions in your project.

#### Cursor

```bash
python3 scripts/install.py adapters /path/to/your-project --agent cursor
```

Generates `README.md` + `.cursor/rules` for Cursor's rule system.

#### OpenCode

```bash
python3 scripts/install.py adapters /path/to/your-project --agent opencode
```

Generates an `AGENTS.md` in your project root.

#### Hermes

```bash
python3 scripts/install.py adapters /path/to/your-project --agent hermes
```

Generates `AGENTS.hermes.md` in your project root. To also mirror skills to `~/.hermes/skills/`:

```bash
python3 scripts/install.py adapters /path/to/your-project --agent hermes --install-user-skills
```

#### OpenClaw

```bash
python3 scripts/install.py adapters /path/to/your-project --agent openclaw
```

Generates `AGENTS.openclaw.md`, `SOUL.md`, `TOOLS.md`, and copies skills to your project.

#### Generic (Any Agent)

```bash
python3 scripts/install.py adapters /path/to/your-project --agent generic
```

Generates a universal `AGENTS.generic.md` that works with any agent supporting markdown-based instructions.

### Scaffold a New Project

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

### Spec Kit (optional)

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

## Quick Start

### Step 1 — Install the Kit

```bash
git clone https://github.com/yichi2077/idea2product-agent-kit.git
cd idea2product-agent-kit
python3 scripts/install.py skills --target claude-code    # install skills to your agent
python3 scripts/install.py scaffold /path/to/my-project   # set up .pipeline/ in your project
python3 scripts/install.py adapters /path/to/my-project --agent claude-code  # generate agent instructions
```

### Step 2 — Describe Your Idea

In your agent, run:

```
run p1
```

The agent walks you through creating `docs/00-idea/idea-brief.md`. This is your raw idea captured in a structured template.

### Step 3 — Run the Pipeline

```
next
```

The agent tells you which phase comes next and what to do. Alternatively, run a specific phase:

```
run p2
```

### Step 4 — Check Status Anytime

```
status
```

Shows current phase, completed phases, pending gates, and due assumptions.

### Step 5 — Approve a Gate

When a phase reaches a gate (Strategy / Product / Architecture / Release), the agent stops, shows you the decision, its confidence, and the open assumptions/risks, and asks you to approve or reject.

By default (**light** gate mode) you approve **right in the agent chat** — tell the agent "approve" with a one-line reason and it records your verdict. No separate terminal.

Want a hard, agent-proof checkpoint instead? Switch to **strict** mode (approval only in a separate real terminal with a challenge code):

```bash
python3 .pipeline/scripts/pipeline.py gate mode strict
```

### Step 6 — Keep Going

```
run p4
run p5
...
run p9
```

Each phase has its own recipe, templates, and domain skills that guide the work.

---

## Phase Reference

| Phase | Name | What It Does | Key Outputs |
|-------|------|-------------|-------------|
| **P1** | Idea Brief | Capture and structure your raw idea into a concise brief | `docs/00-idea/idea-brief.md` |
| **P2** | Strategy Research | Scan existing solutions, analyze market/finance/risk evidence | Market scan, financial model, risk register, assumption register |
| **P3** | Strategy Decision | Compare build/buy/partner/do-nothing with red-team review | Decision memo, product thesis |
| **P4** | Product Discovery | Define target users, jobs-to-be-done, opportunity mapping | JTBD canvas, opportunity tree, lean canvas |
| **P5** | Product Definition | Write PRD, acceptance criteria, user stories, edge cases | PRD, acceptance criteria, user stories, edge case docs |
| **P6** | Architecture Handoff | Evaluate technical options, create architecture decision records | ADRs, design rationale, architecture spec |
| **P7** | Feature Specification | Specify MVP features with test-first approach | Feature specs, test plans, TDD specs |
| **P8** | Build & Release | Execute implementation, code review, verification, launch prep | Working code, launch checklist, GTM plan |
| **P9** | Outcome Review | Measure results against hypothesis, decide next steps | Outcome review, pivot/persevere decision |

> **Note:** P2 and P3 are blocked until a real idea exists in `docs/00-idea/idea-brief.md`. P2 always starts with an existing-solutions scan.

---

## Gate System

Gates are **human-owned decision points** that protect you from rushing past critical commitments. The decision is always yours, and the agent can never *skip* a gate — the next phase stays blocked until your verdict is recorded.

### The 4 Gates

| Gate | After Phase | What You're Deciding |
|------|------------|---------------------|
| **Strategy Gate** | P3 | Is this idea worth pursuing? Should I build, buy, partner, or walk away? |
| **Product Gate** | P5 | Is the product definition solid enough to commit to architecture? |
| **Architecture Gate** | P6 | Is the technical plan sound enough to start building? |
| **Release Gate** | P8 | Is the product ready to ship to real users? |

### Gate Modes

| Mode | How you approve | Guarantee | Best for |
|------|-----------------|-----------|----------|
| **light** (default) | In the agent chat — say "approve" + a one-line reason; the agent records it | Behavioral contract + audit trail; not cryptographically agent-proof | Solo operators who want to stay in flow |
| **strict** | In a **separate real OS terminal**, typing a random challenge code | The agent literally cannot approve (env + TTY checks) | High-stakes or multi-party setups |

Switch anytime: `python3 .pipeline/scripts/pipeline.py gate mode strict` (or `light`). Either way the agent can never *skip* a gate — the next phase stays blocked until a human verdict is recorded.

### How to Approve a Gate

**Light mode (default):** the agent presents the decision and waits. Tell it to approve — e.g. *"approve the strategy gate: the scan found no good existing option and the unit economics hold."* The agent then runs `pipeline_gate.py approve <gate> --rationale "<your reason>"` and continues. To reject, tell it why.

**Strict mode:** open a real OS terminal and run `python3 .pipeline/scripts/pipeline_gate.py approve <gate>`; type the challenge code shown at request time plus a note. (The agent's own terminal is refused by design.)

Approvals are recorded in `.pipeline/state/pipeline-state.yaml` and `.pipeline/state/decision-log.md`.

### Confidence Signals

When requesting a gate, specify your confidence level:

- **high** — Strong evidence, low uncertainty, ready to commit
- **medium** — Reasonable evidence, some open questions remain
- **low** — Proceeding with significant unknowns (allowed but logged)

### Anti-Confirmation Bias

P3 strategy decisions require comparing **build / buy / partner / do-nothing** options. A cross-model red-team review challenges your reasoning before you reach the Strategy Gate.

---

## Utility Skills

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

## Architecture

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
│   ├── p0-resume/             # Resume interrupted pipeline
│   ├── p0-rollback/           # Roll back phases
│   ├── p0-doctor/             # Pipeline health diagnostics
│   ├── p0-retire/             # Graceful pipeline retirement
│   ├── p1-idea-brief/         # Phase 1: Idea capture
│   ├── p2-strategy-research/  # Phase 2: Market/finance/risk research
│   ├── p3-strategy-decision/  # Phase 3: Strategy decision with red-team
│   ├── p4-product-discovery/  # Phase 4: User/needs/opportunity mapping
│   ├── p5-product-definition/ # Phase 5: PRD and specs
│   ├── p6-architecture-handoff/ # Phase 6: Technical architecture
│   ├── p7-feature-specification/ # Phase 7: Feature specs
│   ├── p8-build-release/      # Phase 8: Implementation and launch
│   └── p9-outcome-review/     # Phase 9: Outcome measurement
│
├── pipeline-template/         # Scaffolded into target repo as .pipeline/
│   ├── .pipeline/
│   │   ├── scripts/
│   │   │   ├── pipeline.py        # Pipeline engine — phase execution, state management
│   │   │   ├── pipeline_gate.py   # Gate approval — challenge/response system
│   │   │   ├── link_skills.py     # Link skills into agent skill directories
│   │   │   └── review_due.py      # Check for due reviews and assumptions
│   │   ├── state/                 # Pipeline state files
│   │   ├── pipeline-state.yaml
│   │   ├── assumption-register.yaml
│   │   ├── risk-register.yaml
│   │   └── decision-log.md
│   ├── templates/             # 10 document templates
│   │   ├── idea-brief.md
│   │   ├── decision-memo.md
│   │   ├── hypothesis-tree.md
│   │   ├── issue-tree.md
│   │   ├── product-thesis.md
│   │   ├── red-team-strategy.md
│   │   ├── red-team-architecture.md
│   │   ├── strategy-research-note.md
│   │   ├── launch-gtm-checklist.md
│   │   └── outcome-review.md
│   ├── recipes/               # 9 phase recipes (YAML)
│   │   ├── p1.yaml ... p9.yaml
│   └── vendor/                # Vendored domain skills
│       ├── strategy/          # market-research, financial-analyst, ceo-advisor,
│       │                      # business-investment-advisor, product-discovery
│       ├── product/           # lean-canvas, jtbd, prd, acceptance-criteria,
│       │                      # edge-cases, user-stories, launch-checklist,
│       │                      # hypothesis, experiment-design, instrumentation-spec,
│       │                      # prioritization, problem-statement, opportunity-tree,
│       │                      # design-rationale, adr, spike-summary,
│       │                      # interview-synthesis, pm-critic
│       └── engineering/       # tdd, systematic-debugging, code-review,
│                              # finishing-branch, verification, executing-plans
│
└── agent-adapters/            # Per-agent configuration generators
    ├── claude-code/           # → CLAUDE.md
    ├── codex/                 # → README.md + openai.yaml per skill
    ├── cursor/                # → README.md + .cursor/rules
    ├── opencode/              # → AGENTS.md
    ├── hermes/                # → AGENTS.md + skill mirror
    ├── openclaw/              # → AGENTS.md + SOUL.md + TOOLS.md + skill mirror
    └── generic/               # → AGENTS.md
```

### How It Works

1. **Recipes** (`.pipeline/recipes/p*.yaml`) define each phase — what steps to run, which templates to use, which vendor skills to invoke
2. **Skills** (`skills/p*`) contain the agent instructions (`SKILL.md`) and agent-specific configs (`agents/` directory)
3. **Vendor skills** (`.pipeline/vendor/`) are domain-expert skills the pipeline invokes — strategy analysis, product documentation, engineering practices
4. **State files** (`.pipeline/state/`) track progress, assumptions, risks, and decisions across sessions
5. **Adapters** generate the right instruction files for your agent so it knows how to run the pipeline
6. **Scripts** handle state transitions, gate approvals, and maintenance tasks

---

## FAQ

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

### Why must gate approval happen in a real terminal?

Gates are irreversible decision points. The random challenge + note system prevents accidental approvals and ensures you're making a deliberate, documented choice — not just clicking through prompts.

### Can I customize the templates?

Absolutely. Templates in `.pipeline/templates/` are plain markdown. Edit them to match your workflow. Recipes reference templates by name, so your customizations are picked up automatically.

### How does the anti-confirmation bias work?

P3 (Strategy Decision) forces the agent to compare all viable options — build, buy, partner, and do-nothing — rather than just justifying a pre-made decision. A cross-model red-team review (using `red-team-strategy.md`) challenges the reasoning before you reach the Strategy Gate.

---

## Contributing

Contributions are welcome! Here's how to get involved:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-improvement`)
3. **Commit** your changes with clear messages
4. **Push** to your branch and open a **Pull Request**

### Ideas for Contributions

- New agent adapters (Windsurf, Aider, etc.)
- Additional templates or vendor skills
- Translations of README and templates
- Bug fixes and documentation improvements
- Pipeline recipe optimizations

Please open an issue first for major changes to discuss the approach.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 [yichi2077](https://github.com/yichi2077)

---

<p align="center">
  Built with ❤️ for solo builders who ship.
</p>
