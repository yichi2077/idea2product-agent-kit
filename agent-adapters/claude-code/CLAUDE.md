# idea2product for Claude Code

Use `agent-adapters/common/IDEA2PRODUCT_AGENT_GUIDE.md` as the operating guide for this repository.

Start with:

```bash
python3 .pipeline/scripts/pipeline.py status
python3 .pipeline/scripts/pipeline.py resume
```

When the user asks for a stage, run the matching `P1` through `P9` command. Do not approve gates; only request them and tell the user the manual approval command.

Skills in `.claude/skills` (installed by the adapter) are discovered natively by name; this `.pipeline` command surface is the source of truth for state and gates. Both point at the same workflow.

P2 and P3 stay blocked until `docs/00-idea/idea-brief.md` holds a real idea (the shipped placeholder is rejected on purpose). Gate approval must be done by the user in a plain OS terminal, not this integrated terminal.
