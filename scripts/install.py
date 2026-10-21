#!/usr/bin/env python3
"""Install the bundled skills without replacing an existing skill."""
import argparse
import os
from pathlib import Path
import shutil


def main():
    source = Path(__file__).resolve().parents[1] / "skills"
    default = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=default)
    args = parser.parse_args()
    target = args.destination.expanduser().resolve()
    names = ("film-director", "loop-engineer")
    for name in names:
        if not (source / name / "SKILL.md").is_file():
            parser.error(f"Missing bundled skill: {name}")
        if (target / name).exists():
            parser.error(f"Already exists; nothing copied: {target / name}")
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copytree(source / name, target / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(f"Installed: {target / name}")


if __name__ == "__main__":
    main()
