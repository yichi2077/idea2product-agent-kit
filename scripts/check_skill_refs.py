#!/usr/bin/env python3
"""Check skill-reference integrity for the idea2product kit.

Two checks:

1. HARD (gates CI): every `$skill` token referenced in a recipe
   (`.pipeline/recipes/*.yaml`) must resolve to a bundled skill — a vendor skill, a
   custom skill, or a P0-P10 entry skill. The pipeline executes only what the recipes
   list, so an unresolved recipe reference is a real defect.

2. SOFT (informational): vendored skill *bodies* are excerpts from larger upstream
   collections and may cross-reference sibling skills the kit does not bundle (e.g.
   `superpowers:using-git-worktrees`, `foundation-persona`). Those references never
   drive execution (see THIRD-PARTY-NOTICES "Vendored skills are excerpts"); this
   report just makes the surface visible so a maintainer can spot a *new* reference
   that should have been bundled vs an expected excerpt link.

Usage:
  python3 scripts/check_skill_refs.py            # hard check + soft report (default)
  python3 scripts/check_skill_refs.py --check    # hard check only (terse, CI-friendly)

Exit code is 1 only when the hard check fails; the soft report never fails.
Pure stdlib; same Python the rest of the kit already requires.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
PIPE = KIT_ROOT / "pipeline-template" / ".pipeline"
RECIPES = PIPE / "recipes"
VENDOR = PIPE / "vendor"
CUSTOM = PIPE / "custom-skills"
ENTRY = KIT_ROOT / "skills"
CATEGORIES = ("strategy", "product", "engineering")

RECIPE_REF = re.compile(r"\$([a-z][a-z0-9-]+)")
SP_REF = re.compile(r"superpowers:[a-z][a-z0-9-]+")
SIB_REF = re.compile(
    r"\b(?:foundation|define|deliver|develop|discover|iterate|measure|utility)-[a-z][a-z0-9-]+\b"
)


def resolvable_skills() -> set[str]:
    """All skill names the kit can actually invoke: vendor + custom + P0-P10 entry."""
    names: set[str] = set()
    for cat in CATEGORIES:
        d = VENDOR / cat
        if d.exists():
            names |= {p.name for p in d.iterdir() if p.is_dir()}
    if CUSTOM.exists():
        names |= {p.name for p in CUSTOM.iterdir() if p.is_dir()}
    if ENTRY.exists():
        names |= {p.name for p in ENTRY.glob("idea2product-*") if p.is_dir()}
    return names


def hard_check(resolvable: set[str]) -> list[tuple[str, str]]:
    """[(recipe, unresolved_ref)] for recipe $skill refs that are not bundled."""
    problems: list[tuple[str, str]] = []
    for recipe in sorted(RECIPES.glob("*.yaml")):
        for ref in sorted(set(RECIPE_REF.findall(recipe.read_text(encoding="utf-8")))):
            if ref not in resolvable:
                problems.append((recipe.name, ref))
    return problems


def soft_report(resolvable: set[str]) -> dict[str, set[str]]:
    """{skill: {body cross-refs not bundled in-kit}} across vendored skills."""
    dangling: dict[str, set[str]] = {}
    for cat in CATEGORIES:
        base = VENDOR / cat
        if not base.exists():
            continue
        for d in sorted(p for p in base.iterdir() if p.is_dir()):
            sk = d / "SKILL.md"
            if not sk.exists():
                continue
            text = sk.read_text(encoding="utf-8")
            refs: set[str] = set()
            for m in SP_REF.findall(text):
                if m.split(":", 1)[1] not in resolvable:
                    refs.add(m)
            for m in SIB_REF.findall(text):
                if m != d.name and m not in resolvable:
                    refs.add(m)
            if refs:
                dangling[d.name] = refs
    return dangling


def main() -> int:
    parser = argparse.ArgumentParser(prog="check_skill_refs.py", description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="hard check only (terse, CI-friendly)")
    args = parser.parse_args()

    resolvable = resolvable_skills()
    problems = hard_check(resolvable)
    if problems:
        print("Recipe skill-reference integrity: FAILED")
        for recipe, ref in problems:
            print(f"  unresolved ${ref} referenced in {recipe}")
        print("\nEvery $skill in a recipe must resolve to a bundled vendor/custom/entry skill.")
        rc = 1
    else:
        n = len(list(RECIPES.glob("*.yaml")))
        print(f"✓ Recipe skill-reference integrity: all $skill refs across {n} recipes resolve.")
        rc = 0

    if not args.check:
        dangling = soft_report(resolvable)
        total = sum(len(v) for v in dangling.values())
        print()
        print(f"Excerpt cross-references (informational): vendored skill bodies reference "
              f"{total} sibling skills not bundled here.")
        print("These are expected — vendored skills are verbatim excerpts; execution is "
              "recipe-driven. See .pipeline/vendor/THIRD-PARTY-NOTICES.md.")
        for sk, refs in sorted(dangling.items()):
            print(f"  {sk}: {', '.join(sorted(refs))}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
