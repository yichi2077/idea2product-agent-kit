# idea2product-agent-kit

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Agents](https://img.shields.io/badge/Agents-Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20%7C%20OpenCode%20%7C%20Generic-purple.svg)
![Methodology](https://img.shields.io/badge/Methodology-Anthropic%20Founder's%20Playbook-8A2BE2.svg)
![Version](https://img.shields.io/badge/Version-v2.0.0-orange.svg)

**`idea2product-agent-kit` is the local, enforced, in-chat embodiment of [Anthropic's *Founder's Playbook*](https://claude.com/blog/the-founders-playbook).** It turns the playbook's central discipline — *validate before you build* — into a deterministic phase-gate state machine that your AI coding agent (Claude Code, Cursor, Codex, …) runs **inside the chat**, blocking premature code until the idea, strategy, product, and architecture are validated and approved.

> *"42% of startups fail because they built something nobody wanted — and AI makes that failure mode more likely, not less, because a working prototype is so easily mistaken for proof."* — the problem the *Founder's Playbook* names, and the one this kit is built to prevent.

---

## Table of Contents

- [Why this exists](#why-this-exists)
- [Built on the Founder's Playbook](#built-on-the-founders-playbook)
- [How it works: a phase-gate state machine](#how-it-works-a-phase-gate-state-machine)
- [What makes it different](#what-makes-it-different)
- [Comparison](#comparison)
- [Who it's for & when to use it](#who-its-for--when-to-use-it)
- [Installation & Quick Start](#installation--quick-start)
- [Core mechanics](#core-mechanics)
- [Documentation & customization](#documentation--customization)
- [Contributing](#contributing)
- [License](#license)

---

## Why this exists

In the AI era, products don't die because they're hard to build — they die because someone built a thing nobody wanted. Agentic coding collapses "idea → working prototype" to an afternoon, which makes it *easier* to skip the only thing that matters: evidence that the problem is real.

Left unchecked, an AI coding agent will:
1. Start writing code immediately from a raw prompt.
2. Reinvent solutions that already exist, and miss business/security constraints.
3. Accumulate technical debt with no product definition or architecture to anchor it.
4. Collapse its own context window into refactor loops and a fragmented codebase.

This kit installs a **"shift-left"** discipline: standardize the **Why** and the **What** — *with evidence* — before any **How**. It is deliberately **agent-agnostic** and **local-first**: a lightweight Python state machine (`pipeline.py`) plus Markdown artifacts committed to your repo. No SaaS, no cloud lock-in.

---

## Built on the Founder's Playbook

This kit does not just *reference* the *Founder's Playbook* — it **operationalizes its Idea + MVP methodology** as an enforced workflow. Where the playbook is prose advice an AI can quietly ignore, the kit makes the advice **structural**: required steps, human gates, and checks the engine itself runs.

| Founder's Playbook principle | How the kit enforces it |
| :--- | :--- |
| Turn the idea into a **falsifiable hypothesis** | **P1** idea brief: persona · frequency · quantified loss · current workaround |
| **Map the competitive landscape** (don't be blind to rivals) | **P2** existing-solutions scan: 4 layers (direct / indirect / acquirers / adjacent) + competitor **review-mining** + **steelman-the-rival** |
| Run **customer discovery** — ask about *past behavior*, not future intent | **P4** interview-plan: bias-audited questions, per-interview debrief, every-5 **asymmetry guard** |
| Use AI as a **structured devil's advocate at every stage** | Required red-team / pre-mortem at **P2–P4**, fresh-context PM critic at **P5**, architecture red-team at **P7** |
| *"Confirmation bias now has a research engine"* | **Evidence-provenance** fields + the **confirmation-bias watch**: `doctor` and every gate flag assumptions closed *without user contact*, *without disconfirming evidence*, or a register skewed toward supporting evidence |
| *"The prototype is not evidence — the conversations are"* | **P6 Validation Prototype**: build the single core interaction, test with ~5 target users, decide go / pivot / waive *before* committing to a full build |
| Protect MVP scope — *"real user signal, or founder enthusiasm?"* | **P5** PRD: explicit **non-goals** + an **evidence-gated feature-add bar** |
| A **security review before any user touches it** | **P9** recommended pre-release security review (auth, leakage, injection, CVE deps) |
| Iterate toward **evidence (PMF)**, not perfection | **P6 / P10** PMF instruments: Sean Ellis 40% · effort (push vs pull) · the three R's, plus pivot diagnostics |

> **Scope note (honest):** the kit fully embodies the playbook's **Idea** and **MVP** methodology. The playbook's **Launch / Scale** material is mostly *operations* (founder-attention workflows, growth staffing, compliance programs) and is intentionally **out of scope** — this kit is a 0→1 validation-and-build pipeline, not an ops platform.

---

## How it works: a phase-gate state machine

The workspace is organized into **10 linear phases** and **4 human-in-the-loop gates**. The engine refuses to advance — and especially refuses to let the agent write product code — until each gate is approved.

```
       WHY?                      WHAT?                        HOW?
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  P1 – P3        │────▶│  P4 – P6            │────▶│  P7 – P10           │
│  Strategy &     │     │  Product Definition │     │  Architecture,      │
│  Feasibility    │     │  & Validation       │     │  Specs & Build      │
└─────────────────┘     └─────────────────────┘     └─────────────────────┘
```

| Phase | Description | Key outputs | Gate |
|-------|-------------|-------------|------|
| **P1** | Idea Brief | Falsifiable hypothesis, cost of doing nothing, stop conditions | — |
| **P2** | Strategy Research | Existing-solutions scan (use/buy/partner/build), market analysis, risk register | — |
| **P3** | Strategy Decision | Build/buy/partner memo, strategy red-team, moat check | **Strategy Gate** |
| **P4** | Product Discovery | JTBD, opportunity tree, lean canvas, **interview plan** | — |
| **P5** | Product Definition | PRD (non-goals + evidence-gated scope), user stories, PM critique | **Product Gate** |
| **P6** | **Validation Prototype** | Single core interaction tested with ~5 users; go/pivot/waive *(waivable)* | — |
| **P7** | Architecture Handoff | ADRs, spikes, feature map, traceability matrix | **Architecture Gate** |
| **P8** | Feature Spec | Test-driven, Spec-Kit-ready feature packets | — |
| **P9** | Build & Release | Verified implementation, security review, release decision | **Release Gate** |
| **P10** | Outcome Review | Post-launch hypothesis measurement, PMF signals, pivot/persevere | — |

Everything is driven from **inside your agent's chat**: say `run p1` or `next`, and the agent runs the engine, follows the phase recipe, and produces the Markdown artifacts. The only action a human takes directly is approving a gate.

---

## What makes it different

- 🧭 **Evidence over enthusiasm.** A persistent **assumption register** tracks *how* each claim was validated (real users? experiment? desk research?). The engine's **confirmation-bias watch** flags self-deception before a gate — the one thing prose advice can't do for you.
- 🧪 **A real validation step, not just a prototype.** P6 forces the playbook's hardest lesson into the workflow: build one interaction, put it in front of real people, and let *their behavior* decide go/pivot — before you sink weeks into a full build.
- 🛑 **Deterministic, not autonomous.** A state machine with human gates — no runaway agent loops, no "AI testing AI."
- 🧱 **Low context overhead.** The agent only ever loads the active phase and its deliverables, so context doesn't collapse on long projects.
- 🔒 **Local-first, zero SaaS.** YAML state + Markdown reports live in your Git repo. No external service sees your idea.
- 🤖 **Agent-agnostic & skills-based.** Works across Claude Code, Cursor, Codex, OpenCode, Hermes, OpenClaw, and any AGENTS.md agent — entirely via skills / natural language in the chat.
- 📋 **A source of truth for your agent.** The artifacts from P1–P5 become the agent's grounding context at build time, dramatically cutting hallucination and logical drift.

---

## Comparison

| Aspect | `idea2product` | Ad-hoc agent use (Aider, Claude Code, Cursor) | Multi-agent frameworks (CrewAI, AutoGen) |
| :--- | :--- | :--- | :--- |
| **Execution** | Deterministic state machine; planning docs **before** code | Ad-hoc generation; code first, specs maybe | Autonomous loops; high drift risk |
| **Validation** | **Evidence-tracked** with a confirmation-bias guard | None — vibes | Self-validation (AI checks AI) |
| **Context** | Low — active phase only | High — mixed history collapses context | Very high — chatty agents burn tokens |
| **Quality control** | Human-in-the-loop gates, logged | Manual post-hoc review | Often misses edge cases |
| **Privacy & cost** | Local-first, zero SaaS | Local-first | Often cloud-reliant, high API cost |

---

## Who it's for & when to use it

**Best for**
- **Solo operators & indie hackers** — stops you building for an unvalidated audience (P4) with unvalidated economics (P2).
- **Technical product managers** — generates clean PRDs, acceptance criteria, and architecture handoffs as local Markdown, ready for a dev team.
- **Engineering leads** — enforces a design-first, TDD culture across AI-assisted developers.

**In scope:** 0→1 MVPs · large 1→N feature extensions (billing, OAuth, …) · spikes & feasibility studies (P7).

**Out of scope:** hotfixes & tiny tweaks (a 10-phase pipeline is overkill for a typo) · highly-coupled legacy monoliths · fully autonomous, unattended code generation.

---

## Installation & Quick Start

**Prerequisites:** Python 3.10+ (standard library only) · Git · a compatible coding agent.

### One-shot onboarding (recommended)
```bash
git clone https://github.com/yichi2077/idea2product-agent-kit.git

# Install skills + scaffold the engine + wire your host adapter (auto-detected)
python3 idea2product-agent-kit/scripts/install.py init /path/to/your-project
```

### Or step by step
```bash
# Scaffold the .pipeline engine + docs into your project
python3 idea2product-agent-kit/scripts/install.py scaffold /path/to/your-project

# Install the agent adapter (e.g. Claude Code)
python3 idea2product-agent-kit/scripts/install.py adapters /path/to/your-project --agent claude-code
```
*For Cursor, Codex, OpenCode, Hermes, OpenClaw, or a generic AGENTS.md agent, see the [Technical Deep Dive](docs/TECHNICAL-DEEP-DIVE.md#1-installation-details-per-agent).*

### Start
In your agent's chat, just say:
```
run p1     (or: next)
```
The agent will ask for your idea and walk you through the pipeline. Everything runs in the conversation.

---

## Core mechanics

### Human-in-the-loop gates
Progression is blocked until approval is recorded in `.pipeline/state/pipeline-state.yaml`.
- **Light mode (default):** review the documents in chat, then tell the agent to approve (e.g. *"approve the strategy gate — economics validated"*). The agent records it.
- **Strict mode:** the agent cannot self-approve; the engine requires a challenge code typed in a separate terminal.
  ```bash
  python3 .pipeline/scripts/pipeline.py gate mode strict
  ```

### Confirmation-bias watch
At `doctor` and at every gate, the engine surfaces non-blocking warnings when an assumption was closed **without user contact**, **without any disconfirming evidence**, or when the register skews toward supporting evidence — so you weigh real evidence, not wishful thinking, before committing.

### Integrated diagnostics
```bash
python3 .pipeline/scripts/pipeline.py doctor     # state consistency, missing deliverables, bias watch
python3 .pipeline/scripts/pipeline.py status     # current phase, gates, blockers
python3 .pipeline/scripts/pipeline.py handoff    # consolidated brief: decisions, open assumptions/risks
```

### Git audit trail
At the end of each phase the agent commits the docs + state with a standardized message (e.g. `idea2product: complete P2`), giving you a clean, reviewable history. Nothing is ever pushed automatically.

---

## Documentation & customization

- **Advanced setup, per-agent install, Spec Kit:** [Technical Deep Dive & User Guide](docs/TECHNICAL-DEEP-DIVE.md).
- **Customize the flow:** edit phase recipes in `.pipeline/recipes/p*.yaml` and document templates in `.pipeline/templates/`.
- **Changelog:** [CHANGELOG.md](CHANGELOG.md).

---

## Contributing

1. **Fork** the repo and create a feature branch (`git checkout -b feature/amazing-feature`).
2. Make your changes with a clear description.
3. Before opening a PR, run the integrity checks:
   ```bash
   python3 scripts/sync_bundled_copies.py --check
   python3 scripts/check_skill_refs.py
   ```
4. **Push** and open a **Pull Request**. For major changes, open an issue first to discuss.

---

## License
Licensed under the [MIT License](LICENSE). Copyright (c) 2026 [yichi2077](https://github.com/yichi2077).
