from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
names = [p.name for p in (ROOT / ".agents/skills").iterdir() if p.is_dir()]
dupes = sorted({n for n in names if names.count(n) > 1})
excluded = {"product-research", "product-strategist", "product-manager-toolkit", "agile-product-owner", "cpo-advisor", "cto-advisor", "board-deck-builder", "utility-pm-workflow-orchestrator", "using-superpowers"}
present = sorted(excluded.intersection(names))
if dupes or present:
    print({"duplicate_names": dupes, "excluded_present": present})
    raise SystemExit(1)
print("No trigger conflicts detected.")
