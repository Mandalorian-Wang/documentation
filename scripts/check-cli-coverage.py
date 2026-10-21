#!/usr/bin/env python3
"""Every command the CLI ships must appear in the CLI reference.

The failure this catches is specific and has happened twice: a command group
ships, nobody notices, and the reference silently describes a smaller CLI than
the one users have. `boxlite volume` (four subcommands) and `boxlite network`
went undocumented this way.

Usage:
    python3 scripts/check-cli-coverage.py reference/cli.mdx

Requires the `boxlite` CLI on PATH — it is the source of truth, not the source
tree, because a command can be hidden from help (`completion` is) or renamed by
an alias. Exits non-zero when the reference is missing a command.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path


def cli_commands() -> list[str]:
    """Top-level commands, straight from `boxlite --help`."""
    help_text = subprocess.run(
        ["boxlite", "--help"], capture_output=True, text=True, check=True
    ).stdout
    block = re.search(r"^Commands:\n(.*?)\n\n", help_text, re.S | re.M)
    if not block:
        raise SystemExit("could not find a Commands: block in `boxlite --help`")
    found = [line.split()[0] for line in block.group(1).split("\n") if re.match(r"^  \S", line)]
    return [c for c in found if c != "help"]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    if shutil.which("boxlite") is None:
        print("boxlite is not on PATH — install it before running this check")
        print("  curl -fsSL https://sh.boxlite.ai | sh")
        return 2

    reference = Path(sys.argv[1])
    if not reference.is_file():
        print(f"not a file: {reference}")
        return 2
    doc = reference.read_text(encoding="utf-8")

    commands = cli_commands()
    missing = [c for c in commands if f"boxlite {c}" not in doc]

    print(f"{len(commands)} CLI commands: {' '.join(commands)}")
    if missing:
        for command in missing:
            print(f"{reference}: `boxlite {command}` ships but is not documented")
        print(f"\n{len(missing)} undocumented command(s).")
        return 1
    print(f"{reference}: all documented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
