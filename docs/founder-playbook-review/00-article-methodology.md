# 00 — Article Methodology Extraction

> Source: user-supplied Chinese article distilling **Anthropic's "The Founder's Playbook"** (handbook), focused on its **Chapter 3 validation methodology**, plus the author's own commentary.
> This file captures the article's claims and prompts faithfully so downstream gap-analysis has a stable reference.

## Central thesis

- In the AI era, products die not because they **can't be built**, but because someone **built a thing nobody wanted**.
- Anthropic cites: even **before** the agentic-coding era, **42% of startups failed** because they built something nobody wanted. AI collapses "idea → product" distance to ~zero, so this failure mode gets **worse**, not better.
- **A prototype's existence is not evidence.** It is a prop — a stress-test instrument you take into conversations with real people. **The conversations are the evidence.**
- AI's role: **not autopilot — an on-demand expert** that helps you think more rigorously, research faster, and face disconfirming evidence more honestly. **The "is it worth building" judgment is always yours.**
- You will never get certainty at the idea stage; **waiting for certainty is itself a failure mode.** Goal = enough qualitative evidence to make "commit to MVP" a *reasoned decision*, not an act of faith.
- Closing line: in 2026 the most valuable thing is **not what you can build, but what you choose to build.** AI flattened the build barrier; the **judgment barrier rose.**

## The 6-step validation flow

### Step 1 — Turn the idea from a *feeling* into a *hypothesis*
- Most skipped, most fatal step. "Expense reports are annoying, I want to build a tool" is an **observation, not a hypothesis** — not specific enough to be validated or falsified.
- Target hypothesis shape: **`[specific persona]` in `[specific scenario]` every `[frequency]` hits `[specific problem]`, because `[specific cause]`, costing them `[specific loss]`.**
- Prompt (paraphrased) asks AI to resolve: (1) exactly **who** (title, company type, team size); (2) **how often**; (3) **severity / can it be quantified**; (4) **current workaround & where it hurts**.
- Example transform: "expense reports are annoying" → "finance managers at mid-market companies spend 4+ hrs/week reconciling expense reports because their tool doesn't integrate with accounting software, edits are scattered across email threads, with no version control."

### Step 2 — Make the AI argue *against* you (don't let it help you self-deceive)
- Sharpest insight: **"confirmation bias now has a research engine."** Ask AI to validate your idea and it will *find supporting evidence* and the TAM number that makes your market look fundable — not malice, just following instructions.
- Antidote: aim the same tool the opposite way. Prompt asks AI to be a **brutal investor** whose job is to find why this fails, attacking on: (1) does the problem really exist or is it your bias amplifying it; (2) even if real, will users *pay* vs. tolerate the status quo; (3) which dead competitors tried this & why they failed; (4) structural barriers (tech/regulatory/habit); (5) the single strongest "don't build this" reason.
- **Devil's-advocate AI should run at every stage, not just ideation.** Otherwise you build "an exquisite, well-researched self-deception system."

### Step 3 — Map the competitive landscape (don't only watch direct rivals)
- Names **"competitor blindness"**: over-focused on your own vision/execution, you systematically underestimate others.
- **3 sub-steps:**
  1. **4-layer landscape scan:** ① direct competitors ② indirect (different method, same problem) ③ potential acquirers (big cos with adjacent capability who could enter) ④ adjacent players (not here now, could move in). Demand concrete names + their core approach per layer.
  2. **Mine competitor reviews** (App Store, G2, Reddit, Zhihu) for the **top-5 recurring pain points / complaints** → free qualitative research on rivals' users. Which do *my* hypothesis solve? Which did I not anticipate?
  3. **Steelman the rival:** "Make the most persuasive case for why `[strongest competitor]` succeeds and I fail. Is my differentiation actually a moat? Why would users pick them over me?"

### Step 4 — Design customer-discovery interviews (right people, right questions)
- Memorable rule: novices ask a **future-facing generic** question ("would you use something like this?"); you must probe **past real experience** ("tell me about the last time you hit this problem").
  - ❌ "Would you use this?"  ✅ "What happened the last time you had this problem?"
  - What people *say* they'd do vs. what they *actually* do diverges wildly.
- **3 sub-steps:**
  1. **Define who to interview:** ideal-interviewee persona (title, company type, team size); which seniority feels the pain most acutely; where they congregate (communities, LinkedIn groups, Slack workspaces, conferences); priority order of who to contact first for max signal.
  2. **Design/audit questions:** write a first draft, then have AI flag **leading / too-broad / socially-desirable-answer-inducing** questions and rewrite them to probe past behavior; also design **follow-up probes** for the 2–3 moments interviewees will most likely dodge.
  3. **Post-interview debrief** (per interview): what confirmed the hypothesis; what challenged it; what genuinely surprised you; **am I reading the data for what I want to hear, or for what it actually says?**
- **Cadence:** synthesize every **5 interviews**. **Asymmetry warning:** if your "supports my hypothesis" list is clearly longer than the "challenges it" list, suspect you — is the asymmetry real in the data or wishful in your head?

### Step 5 — Stress-test the solution design
- After validated problem + competitive map + qualitative evidence, design the solution — but stress-test before building.
- Prompt: identify the **3 assumptions the design most depends on**; per assumption: (1) what must be true for it to hold; (2) consequence if it fails; (3) fastest way to validate/refute it.
- **Killer check:** "Is what this solution actually solves the problem the *validation revealed*, or the problem I *thought* I had walking in? They may not be the same." — founders who discover the real problem differs often suppress it because of sunk emotional investment.

### Step 6 — Build a minimal prototype: ONE interaction, give it to 5 users
- Not a full product. Define **the single core, indispensable interaction** — "if a user could experience only one feature to decide if this has value, which one?" Cut everything else.
- Build that one interaction (e.g., with Claude Code). Give to **5 people matching the validated target persona.** Observe reactions, listen.
- Those 5 conversations decide: push forward, or back to the drawing board.

## Caveats the author flags
- The flow is **not** a substitute for your judgment, your user empathy, or actually talking to people yourself.
- It helps you learn — at lowest cost, shortest time — whether an idea is worth the investment. It can't replace the final "worth it?" call.
