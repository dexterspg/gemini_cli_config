#!/usr/bin/env python3
"""
Switch model assignments for Gemini agents.

Usage:
  python switch-models.py                          # list current models
  python switch-models.py --all flash              # set all agents to flash
  python switch-models.py --all pro                # set all agents to pro
  python switch-models.py --from flash --to pro    # swap flash -> pro across all
  python switch-models.py --agent agent-debugger --model flash  # single agent
"""

import re
import sys
import argparse
from pathlib import Path

AGENTS_DIR = Path(__file__).parent / "agents"

KNOWN_MODELS = [
    "flash",
    "pro",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]


def get_agents() -> list[Path]:
    return sorted(AGENTS_DIR.glob("*.md"))


def read_model(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^model:\s*(.+)$", line)
        if m:
            return m.group(1).strip()
    return None


def set_model(path: Path, new_model: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, count = re.subn(r"^(model:\s*)(.+)$", rf"\g<1>{new_model}", text, flags=re.MULTILINE)
    if count == 0:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def list_agents():
    agents = get_agents()
    max_name = max(len(p.stem) for p in agents)
    print(f"\n{'Agent':<{max_name}}  Model")
    print("-" * (max_name + 20))
    for path in agents:
        model = read_model(path) or "(not set)"
        print(f"{path.stem:<{max_name}}  {model}")
    print()


def switch_all(new_model: str):
    agents = get_agents()
    for path in agents:
        old = read_model(path)
        set_model(path, new_model)
        print(f"  {path.stem}: {old} -> {new_model}")
    print(f"\nUpdated {len(agents)} agent(s) to '{new_model}'.")


def switch_from_to(from_model: str, to_model: str):
    agents = get_agents()
    changed = 0
    for path in agents:
        current = read_model(path)
        if current == from_model:
            set_model(path, to_model)
            print(f"  {path.stem}: {from_model} -> {to_model}")
            changed += 1
        else:
            print(f"  {path.stem}: {current} (skipped)")
    print(f"\nUpdated {changed} agent(s) from '{from_model}' to '{to_model}'.")


def switch_one(agent_name: str, new_model: str):
    # Accept with or without .md extension
    name = agent_name.removesuffix(".md")
    path = AGENTS_DIR / f"{name}.md"
    if not path.exists():
        print(f"Error: agent '{name}' not found in {AGENTS_DIR}")
        sys.exit(1)
    old = read_model(path)
    set_model(path, new_model)
    print(f"  {name}: {old} -> {new_model}")


def main():
    parser = argparse.ArgumentParser(
        description="Switch model assignments in Gemini agent frontmatter."
    )
    parser.add_argument("--all", metavar="MODEL", help="Set all agents to MODEL")
    parser.add_argument("--from", dest="from_model", metavar="MODEL", help="Source model to replace")
    parser.add_argument("--to", dest="to_model", metavar="MODEL", help="Target model to use")
    parser.add_argument("--agent", metavar="NAME", help="Target a single agent by name")
    parser.add_argument("--model", metavar="MODEL", help="Model to assign (used with --agent)")

    args = parser.parse_args()

    if args.all:
        switch_all(args.all)
    elif args.from_model and args.to_model:
        switch_from_to(args.from_model, args.to_model)
    elif args.from_model or args.to_model:
        parser.error("--from and --to must be used together")
    elif args.agent and args.model:
        switch_one(args.agent, args.model)
    elif args.agent:
        parser.error("--agent requires --model")
    else:
        list_agents()


if __name__ == "__main__":
    main()
