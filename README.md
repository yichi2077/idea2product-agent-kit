# idea2product-agent-kit

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Agents](https://img.shields.io/badge/Agents-Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20%7C%20Generic-purple.svg)
![Version](https://img.shields.io/badge/Version-v1.1.0-orange.svg)

`idea2product-agent-kit` is a local, state-driven workflow manager that guides AI coding agents (Claude Code, Cursor, Codex, etc.) through a structured software engineering lifecycle.

By running a lightweight Python state machine (`pipeline.py`) in your project, it prevents coding agents from writing code prematurely. It enforces planning, research, product specification, and architecture design in markdown before code generation begins.

---

## Table of Contents

- [Background](#background)
  - [The Problem: Agent Drift](#the-problem-agent-drift)
  - [The "Shift-Left" Philosophy](#the-shift-left-philosophy)
  - [The Value for "Vibe Coders"](#the-value-for-vibe-coders)
- [The Solution: A Phase-Gate State Machine](#the-solution-a-phase-gate-state-machine)
- [Core Comparisons \& Advantages](#core-comparisons--advantages)
- [Applicable Scope \& Scenarios](#applicable-scope--scenarios)
  - [Project Boundary (Scope)](#project-boundary-scope)
  - [Recommended Scenarios](#recommended-scenarios)
- [Installation \& Quick Start](#installation--quick-start)
- [Core Mechanics](#core-mechanics)
  - [Human-in-the-Loop Gates](#human-in-the-loop-gates)
  - [Auto-Git Commits](#auto-git-commits)
  - [Integrated Diagnostics](#integrated-diagnostics)
- [Documentation \& Customization](#documentation--customization)
- [Contributing](#contributing)
- [License](#license)

---

## Background

### The Problem: Agent Drift
When working with coding agents, a common pitfall is the lack of structured planning:
1. The agent starts writing code immediately based on a raw prompt.
2. Without a strategy scan, it may reinvent existing solutions or miss critical constraints.
3. Without a product definition or technical architecture, code debt accumulates rapidly.
4. The agent's context window collapses, resulting in refactoring loops and a fragmented codebase.

### The "Shift-Left" Philosophy
Most agentic tools focus heavily on the **"How"** (implementation, TDD, code generation). `idea2product` enforces a **Shift-Left** approach, standardizing the **"Why"** and **"What"** before any engineering decisions are made. 

By defining the business strategy and product scope first, you eliminate wasted engineering hours on unfeasible or redundant ideas.

```
       WHY?                    WHAT?                     HOW?
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────┐
│  P1 - P3        │────▶│  P4 - P6        │────▶│  P7 - P10           │
│  Strategy &     │     │  Product        │     │  Architecture,      │
│  Feasibility    │     │  Definition     │     │  Specs & Build      │
└─────────────────┘     └─────────────────┘     └─────────────────────┘
```

### The Value for "Vibe Coders"
If you build software based on intuition and rapid agent chats (Vibe Coding), this framework acts as a stabilizer:
*   **Requirements Consolidation**: It forces you to map target user needs (P4 opportunity trees) and business feasibility (P2 financial models) to prevent scope creep.
*   **A "Source of Truth" for your Agent**: 90% of agent code generation errors stem from a lack of context regarding business intent. The markdown artifacts created in phases P1-P5 (PRDs, risk registers) serve as a structured knowledge base. When you reach the build phase (P8), the agent references these local files, significantly reducing logical drift and hallucinations.

---

## The Solution: A Phase-Gate State Machine

`idea2product-agent-kit` organizes the workspace into **10 linear phases** and **4 human-in-the-loop gates**. The CLI engine blocks the agent from progressing to code generation until the preceding design and architecture gates are manually approved.

### The 10-Phase Workflow

| Phase | Description | Outputs | Gate Check |
|-------|-------------|---------|------------|
| **P1** | Idea Brief | `docs/00-idea/idea-brief.md` | - |
| **P2** | Strategy Research | Solutions scan, market analysis, risk register | - |
| **P3** | Strategy Decision | Build/buy/partner memo, product thesis | **Strategy Gate** |
| **P4** | Product Discovery | JTBD canvas, opportunity tree, lean canvas | - |
| **P5** | Product Definition | PRD, user stories, acceptance criteria | **Product Gate** |
| **P6** | Validation Prototype | Single core interaction tested with ~5 users (waivable) | - |
| **P7** | Architecture Handoff| ADRs, spikes, traceability matrix | **Architecture Gate** |
| **P8** | Feature Spec | Test-driven feature specifications | - |
| **P9** | Build & Release | Verified implementation, release checklist | **Release Gate** |
| **P10** | Outcome Review | Post-launch hypothesis measurement | - |

---

## Core Comparisons & Advantages

| Feature / Aspect | `idea2product` Workflow | Ad-hoc Agent Usage (Aider, Claude Code, Cursor) | Multi-Agent Frameworks (CrewAI, AutoGen) |
| :--- | :--- | :--- | :--- |
| **Execution Path** | **Deterministic state machine**. Enforces planning documents before code. | **Ad-hoc generation**. Starts writing code immediately without specifications. | **Autonomous loops**. High risk of agent loop drift and unpredictable code quality. |
| **Context Overhead** | **Low**. Focuses agent context only on the active phase and deliverables. | **High**. Prompts quickly accumulate mixed history, leading to context collapse. | **Extremely High**. Multiple agents chatting increases token cost and noise. |
| **Quality Control** | **Human-in-the-loop gates**. Blocks progression until human approvals are logged. | **Manual review post-generation**. Harder to catch architectural flaws early. | **Self-validation**. Relies on AI-testing-AI, which often misses edge cases. |
| **Privacy & Cost** | **Local-first (Zero SaaS)**. YAML state and Markdown reports committed to Git. | **Local-first**. | **Often Cloud-reliant**. Can run up high API fees during recursive runs. |

---

## Applicable Scope & Scenarios

### Project Boundary (Scope)
*   **In-Scope (What it's built for):**
    *   **0-to-1 MVP Development:** Setting up a clean, architected repository with validated assumptions.
    *   **Large Feature Extensions (1-to-N):** Isolating a major new feature (e.g., adding billing or OAuth) and running it through research and specification before coding.
    *   **Spikes & Feasibility Studies:** Exploring technical unknowns using Phase 6 Spikes.
*   **Out-of-Scope (What it's NOT for):**
    *   **Hotfixes & Tiny Tweaks:** Running a 9-phase pipeline to fix a typo or modify a single line of CSS adds unnecessary overhead.
    *   **Monolithic Legacy Systems:** Highly coupled codebases where linear phase-gate transitions are too rigid.
    *   **Autonomous Code Generation:** This kit does not generate code without human validation; it is strictly an interactive pipeline.

### Recommended Scenarios
*   **Solo Operators & Indie Hackers:** Restrains you from writing code for features without validating target users (P4) and unit economics (P2).
*   **Technical Product Managers:** Generates clean PRDs, acceptance criteria, and architecture decisions in local markdown files, ready to hand off to developers.
*   **Engineering Leads:** Enforces a standardized TDD (Test-Driven Development) and design-first culture across AI-assisted developer workflows.

---

## Installation & Quick Start

### Prerequisites
- **Python 3.10+** (standard library only)
- **Git**
- A compatible coding agent (Claude Code, Cursor, etc.)

### 1. Installation
Run the installer script to scaffold the `.pipeline` folder and generate the configuration adapter for your agent:

```bash
# Clone the repository
git clone https://github.com/yichi2077/idea2product-agent-kit.git

# Scaffold your target project directory
python3 idea2product-agent-kit/scripts/install.py scaffold /path/to/your-project

# Install agent instructions (e.g., Claude Code, Cursor)
python3 idea2product-agent-kit/scripts/install.py adapters /path/to/your-project --agent claude-code
```

*For other agents (Cursor, Codex, Hermes, OpenClaw, Generic), refer to the [Technical Deep Dive](docs/TECHNICAL-DEEP-DIVE.md#1-installation-details-per-agent).*

### 2. Start a Project
In your coding agent, navigate to your project directory and start the guided flow:

```bash
# Run the first phase
python3 .pipeline/scripts/pipeline.py run p1
```
*(Or simply tell your agent: `run p1` or `next` if you have linked the instructions).*

---

## Core Mechanics

### Human-in-the-Loop Gates
The state machine blocks phase progression until approval is recorded in `.pipeline/state/pipeline-state.yaml`.
- **Light Mode (Default)**: Review documents in the agent's chat, then instruct the agent to approve (e.g., `"approve the strategy gate with rationale: economics validated"`). The agent runs `pipeline_gate.py` to record it.
- **Strict Mode**: Prevent the agent from self-approving. The engine requires a challenge code entered manually in a separate, physical terminal. Switch mode using:
  ```bash
  python3 .pipeline/scripts/pipeline.py gate mode strict
  ```

### Auto-Git Commits
To keep a clean audit trail, the state machine automatically commits all documentation and state changes at the end of each phase with a standardized message:
`[pipeline] complete P2: Strategy Research`

### Integrated Diagnostics
Run the health check command to verify state consistency, detect missing deliverables, or audit unresolved assumptions:
```bash
python3 .pipeline/scripts/pipeline.py doctor
```

---

## Documentation & Customization

- **Advanced Options**: Custom adapters, project upgrades, and Spec Kit integration details are documented in the **[Technical Deep Dive & User Guide](docs/TECHNICAL-DEEP-DIVE.md)**.
- **Templates & Recipes**: You can customize phase workflows in `.pipeline/recipes/p*.yaml` and change document templates in `.pipeline/templates/`.

---

## Contributing

We welcome contributions from the community to improve the pipeline engine, adapters, and templates.

1. **Fork** the repository.
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`).
3. **Commit** your changes with clear description.
4. **Push** to the branch and open a **Pull Request**.

Before opening a PR, run the kit integrity checks: `python3 scripts/sync_bundled_copies.py --check` and `python3 scripts/check_skill_refs.py --check`.

For major modifications, please open an issue first to discuss your proposed changes.

---

## License
Licensed under the [MIT License](LICENSE). Copyright (c) 2026 [yichi2077](https://github.com/yichi2077).
