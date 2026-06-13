# idea2product Agent Kit

> 中文说明：[README.zh-CN.md](README.zh-CN.md)

A portable, agent-driven workflow that takes one person from a **raw idea** all the
way to a **shipped product** — through strategy, product definition, architecture,
and delivery — without losing rigor and without drowning in documents.

It is built for the solo operator who wears three hats at once: **strategy analyst**,
**product manager**, and **engineer**. The kit bridges those three roles so the same
idea flows cleanly from "is this even worth doing?" to "here is the merged, tested
feature," with explicit human decision points in between.

It runs as a set of **skills** inside coding agents (Claude Code and Codex today,
with adapters for Cursor, OpenCode, Hermes, OpenClaw, and any AGENTS.md host).

---

## What problem it solves

Working alone, the easy failure mode is to fall in love with an idea and rush it
into code — skipping the strategy and product thinking that would have killed or
reshaped it. The opposite failure is to generate endless analysis documents that
never become a product.

This kit forces a disciplined **expand → contract** rhythm and makes you stop at the
decisions that matter:

```
Idea ──expand──▶ Strategy ──decide──▶ Product ──define──▶ Architecture ──build──▶ Outcome
        market          KILL/HOLD/        PRD,            ADRs, feature      ship &
        finance         EXPLORE/          discovery,      map, spikes        measure
        risk            COMMIT            validation
```

Three expansion→contraction funnels:

1. **Idea expands** into market / finance / risk evidence, then **contracts** to a strategy decision.
2. **Strategy expands** into product options, then **contracts** to a defined product.
3. **Product expands** into technical options, then **contracts** to an architecture and delivery.

---

## Core concepts

**9 phases (P1–P9).** Idea capture → strategy analysis → strategy decision → product
discovery → product definition → architecture handoff → feature spec → build/release →
outcome review.

**4 gates.** `Strategy`, `Product`, `Architecture`, `Release`. A gate is a hard stop
that **only a human can approve**. Agents may *request* a gate and prepare the
decision context; they can never approve one.

**3 modes.** Pick the ceremony that fits the stakes:
- **Light** — personal tools and low-risk prototypes (P1 → P7 → P8, minimal gates).
- **Standard** — real product MVPs (full P1–P9, all four gates).
- **High-Assurance** — regulated / sensitive / irreversible work (adds full financial
  models, security & privacy review, cross-model red-teaming, supply-chain audit).

**Single source of truth.** The Decision Memo owns the strategy decision, the PRD owns
the product, ADRs own the technical direction, and Spec Kit specs own the features.
Slides and issues are *expressions* of those, never the source.

**Real-idea guard.** P2 and P3 stay blocked until `docs/00-idea/idea-brief.md` holds a
real idea — a shipped placeholder is rejected on purpose, so you can't rubber-stamp a
fabricated idea through the strategy gate.

**Anti-confirmation-bias by design.** Strategy decisions compare build / buy / partner /
do-nothing, and Standard+ runs a cross-model red-team review of the recommendation.

---

## What's in the box

- **`skills/`** — 12 installable entry skills:
  - `idea2product-p0-guided-flow` — the one-call orchestrator that reads state and tells you the next step.
  - `idea2product-p1-…` through `…-p9-outcome-review` — one skill per phase.
  - `idea2product-p0-status` / `idea2product-p0-resume` — report / continue.
- **`pipeline-template/`** — the repo-local `.pipeline` engine that gets scaffolded into
  your project: deterministic Python CLI, 9 phase recipes, state registers
  (assumptions, risks, decisions), vendored domain skills, and user-facing docs.
- **`agent-adapters/`** — host wiring for Claude Code, Codex, Cursor, OpenCode, Hermes,
  OpenClaw, and generic AGENTS.md agents.
- **`scripts/`** — install, scaffold, and adapter helpers.

The pipeline's domain expertise comes from **vendored, license-tracked skills** pinned
to fixed commits: strategy skills (market research, financial analysis, CEO advisor,
etc.), product skills (lean canvas, JTBD, PRD, acceptance criteria, etc.), and
engineering discipline skills (TDD, systematic debugging, code review).

---

## Requirements

- **Python 3.10+** — the only thing you need. The installer and all pipeline commands
  (`status`, `run`, `gate`, `stage`, `mode`) use only the Python standard library. No
  PowerShell, no Node, no pip install for everyday use. Works on Windows, macOS, Linux.
- **Git** — for history and to tag gate approvals.

---

## Install (one step, any OS)

The installer is `scripts/install.py` and runs the same on every platform.

### Claude Code

```bash
python3 scripts/install.py skills --target claude-code
```

This copies the 12 skills into `~/.claude/skills`, where Claude Code discovers them by
name. Open a new thread if they don't appear immediately.

### Codex

```bash
python3 scripts/install.py skills --target codex
```

Installs into `~/.agents/skills`. Invoke skills explicitly with `$skill-name`.

### Both at once

```bash
python3 scripts/install.py skills
```

> Windows users may also use the `.ps1` wrappers in `scripts/` (e.g.
> `install_user_skills.ps1`); they just forward to `install.py`.

---

## Quick start

You drive this kit by **talking to your coding agent and invoking skills** — the
agent runs the pipeline for you. You don't type pipeline commands yourself, with
one deliberate exception: gate approval (below).

1. Open any project folder (empty is fine).
2. Ask the agent to start the guided flow — e.g. *"Use idea2product-p0-guided-flow to begin."*
   On first use it auto-creates `.pipeline/` and `docs/` only in an empty directory
   (or a `.git`-only empty repo). In a non-empty repo, tell the agent to run
   guided-flow `init .` (or scaffold explicitly) so the wrong repository is not dirtied.
3. Give the agent your real idea; it captures it in `docs/00-idea/idea-brief.md`
   during P1. (Until a real idea exists, P2/P3 stay blocked.)
4. Keep going by asking the agent to proceed — it always tells you the next correct
   step and runs it. The skills you invoke by name:

```text
idea2product-p0-guided-flow   one call: orient, then run the next step
idea2product-p0-status        report where you are (+ stale-output warnings)
idea2product-p0-resume        re-orient (handoff brief) and continue
idea2product-p1-idea-expansion … idea2product-p9-outcome-review
```

To pick up after a break or in a fresh session, just ask the agent to resume: it
runs the read-only **handoff brief** — decisions already made, open questions,
what's gone stale, and the next step — and summarizes it. If downstream work
invalidates an upstream phase, ask the agent to **reopen** that phase; it reworks
the state cleanly instead of hand-editing it.

### Gates are yours to approve

Gates are the one place you act directly. The agent *prepares and requests* a gate
(stating its confidence in the decision context it assembled); **you** approve or
reject in a **plain OS terminal** (PowerShell/cmd/bash opened directly — **not** the
agent's integrated terminal, which the command refuses on purpose):

```powershell
python .pipeline/scripts/pipeline_gate.py approve strategy
python .pipeline/scripts/pipeline_gate.py reject strategy
```

Approval requires the gate name, the random challenge printed at request time, and a
note. The agent's stated confidence is shown to you first, so you can vary your
scrutiny. A successful approval records the approver, time, and commit, and creates an
annotated `i2p-gate-<gate>-<timestamp>` git tag. A rejected gate can be re-opened by
requesting it again.

---

## Other hosts and project-scoped install

Install host adapters into a target repository (and, for Claude Code, repo-scoped
skills under `.claude/skills` that travel with the project):

```bash
python3 scripts/install.py adapters /path/to/repo --agent claude-code
python3 scripts/install.py adapters /path/to/repo --agent cursor
python3 scripts/install.py adapters /path/to/repo --agent all
```

To pre-create the `.pipeline` engine in a repo without going through a skill:

```bash
python3 scripts/install.py scaffold /path/to/repo
```
