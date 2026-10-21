#!/usr/bin/env python3
"""Structural lint for the BoxLite docs tree.

Three rules, each chosen because it is *mechanically decidable* — a hit is a
defect, never a judgement call. Anything needing taste stays out of CI.

  1. nav-target     every page in docs.json resolves to a file on disk
  2. mdx-hazard     no bare <PLACEHOLDER> or {expression} in prose
  3. table-default  no empty cell under a parameter table's Default column

Usage:
    python3 scripts/check-structure.py <docs_dir>

Exits non-zero on any violation, so it can gate CI.

Rule 2 is the one that actually breaks the build: `.mdx` is JSX-flavoured, so a
bare `<YOUR_API_KEY>` parses as a tag and `{id}` as a JS expression. Both are
fine inside backticks or a fence, which is what the docs are supposed to do.

Rule 3 exists because "Default" is the column readers scan to decide whether an
argument is optional. A blank cell is not "no default" — write an em dash.
"""

import json
import re
import sys
from pathlib import Path

SKIP_FILES = {"CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md", "STYLE_GUIDE.md"}

# An all-caps tag name is a placeholder someone forgot to wrap. Real Mintlify
# components are CamelCase (<Note>, <CardGroup>), so they cannot match.
BARE_TAG = re.compile(r"<[A-Z][A-Z0-9_]+>")

# A brace expression in prose. `cols={2}` and friends are JSX attributes, so a
# brace directly preceded by `=` is excluded.
BARE_BRACE = re.compile(r"(?<![=`\w]){[^{}\n]{1,80}}")


def strip_code(line: str) -> str:
    """Blank out `inline code` spans: a hazard inside backticks is intended."""
    return re.sub(r"`[^`]*`", "``", line)


def iter_prose(path: Path):
    """Yield (lineno, raw, prose) for lines outside fenced code blocks."""
    in_fence = False
    for number, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield number, raw, strip_code(raw)


def check_mdx_hazards(path: Path) -> list[str]:
    out = []
    in_jsx = False
    for number, raw, prose in iter_prose(path):
        # Skip multi-line JSX component tags, where braces are attributes.
        stripped = raw.lstrip()
        if in_jsx:
            if ">" in raw:
                in_jsx = False
            continue
        if stripped.startswith("<") and ">" not in raw:
            in_jsx = True
            continue
        for found in BARE_TAG.findall(prose):
            out.append(f"{path}:{number}: bare JSX tag {found} — wrap it in backticks")
        for found in BARE_BRACE.findall(prose):
            out.append(f"{path}:{number}: bare brace expression {found} — wrap it in backticks")
    return out


def check_table_defaults(path: Path) -> list[str]:
    out = []
    default_col = None
    for number, raw, _ in iter_prose(path):
        if not raw.lstrip().startswith("|"):
            default_col = None
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if default_col is None:
            if any(c.strip("*` ").lower() == "default" for c in cells):
                default_col = next(
                    i for i, c in enumerate(cells) if c.strip("*` ").lower() == "default"
                )
            continue
        if set(raw.replace("|", "").strip()) <= set("-: "):  # separator row
            continue
        if default_col < len(cells) and not cells[default_col]:
            out.append(
                f"{path}:{number}: empty Default cell — write the value, or an em dash"
            )
    return out


def check_nav_targets(root: Path) -> list[str]:
    config = root / "docs.json"
    if not config.is_file():
        return [f"{config}: missing"]
    data = json.loads(config.read_text(encoding="utf-8"))
    out = []
    seen = set()

    def page(slug):
        """A string inside a `pages` array is a route; anything else is a label."""
        if slug.startswith(("http://", "https://")) or slug in seen:
            return
        seen.add(slug)
        if not any((root / f"{slug}{ext}").is_file() for ext in (".mdx", ".md")):
            out.append(f"docs.json: navigation points at '{slug}', which has no file")

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "pages" and isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            page(item)
                        else:
                            walk(item)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data.get("navigation", {}))
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 2

    pages = sorted(
        p
        for p in [*root.rglob("*.md"), *root.rglob("*.mdx")]
        if not (p.parent == root and p.name in SKIP_FILES)
        and "scripts" not in p.parts
        and "node_modules" not in p.parts
        and ".git" not in p.parts
    )

    problems = check_nav_targets(root)
    for path in pages:
        problems += check_mdx_hazards(path)
        problems += check_table_defaults(path)

    for line in problems:
        print(line)
    if problems:
        print(f"\n{len(problems)} structural violation(s).")
        return 1
    print(f"{root}: {len(pages)} pages checked — nav targets, MDX hazards, table defaults all clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
