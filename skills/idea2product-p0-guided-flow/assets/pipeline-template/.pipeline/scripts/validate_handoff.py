from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
required = [ROOT / "docs/20-product/prd.md", ROOT / "docs/30-architecture/traceability-matrix.yaml"]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    print("Missing handoff inputs: " + ", ".join(missing))
    raise SystemExit(1)
print("Handoff inputs present.")
