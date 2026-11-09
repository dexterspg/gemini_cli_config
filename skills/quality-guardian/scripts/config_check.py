"""Mechanical checks for ~/.gemini config edits. Read-only.
Exit 0 = pass, or nothing uncommitted to check; 1 = problems found; 2 = NOT CHECKED (git, PyYAML or agents/ unavailable).
Run: python -X utf8 -I C:/Users/<username>/.gemini/skills/quality-guardian/scripts/config_check.py [--all]
Without --all it prints one line and exits when git shows no uncommitted change under agents/, skills/ or GEMINI.md.
Checks: skill frontmatter (check_frontmatter.py); agent frontmatter (name matches file, description present, no color:, valid Gemini model);
identity line in agents; removed names still referenced; agent-* names with no agents/ file; stated agent count."""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
REMOVED = ["agent-gemini", "agent-persona-reviewer", "agent-product-strategist", "agent-jira-content-creator", "jira-content-creator", "persona-reviewer"]
HISTORY = ("skills/quality-guardian/EVIDENCE-agent-design.md", "skills/claude-bridge/SKILL.md")
NOT_AGENTS = ("agent-nla", "agent-channel", "agent-provenance", "agent-config", "agent-smoke", "agent-brief",
              "agent-no-identity", "agent-to-", "agent-skill", "agent-persona", "agent-loop", "agent-name", "agent-internal",
              "agent-generated", "agent-script")
VALID_MODELS = {"flash", "pro", "flash_lite", "inherit"}
SCAN = ("agents", "skills", "GEMINI.md")
TRIGGER = SCAN


def run(*a):
    try:
        return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    except OSError:
        return None


def changed():
    """True / False, or None when git failed (not a pass)."""
    r = run("git", "status", "--porcelain", "--", *TRIGGER)
    if r is None or r.returncode != 0:
        return None
    return bool(r.stdout.strip())


def scan_files():
    for s in SCAN:
        p = ROOT / s
        for f in ([p] if p.is_file() else p.rglob("*.md") if p.is_dir() else []):
            rel = f.relative_to(ROOT).as_posix()
            if rel in HISTORY or "/results/" in rel or "/synced/" in rel:
                continue
            yield f, rel


def main():
    if "--all" not in sys.argv:
        c = changed()
        if c is None:
            print("NOT CHECKED: git failed or is not available"); return 2
        if not c:
            print("config_check: no uncommitted config changes, skipped"); return 0
    bad = []
    agent_dir = ROOT / "agents"
    agents = {f.stem for f in agent_dir.glob("*.md")} if agent_dir.is_dir() else set()
    if not agents:
        print("NOT CHECKED: agents/ is missing or empty"); return 2
    for target in ("skills",):
        if not (ROOT / target).is_dir():
            continue
        r = run(sys.executable, "-I", str(ROOT / "skills/quality-guardian/scripts/check_frontmatter.py"), str(ROOT / target))
        if r is None or r.returncode not in (0, 1) or (r.returncode == 1 and not r.stdout.strip()):
            print(f"NOT CHECKED: frontmatter check failed on {target}: " + ((r.stdout + r.stderr).strip()[:200] if r else "cannot run")); return 2
        bad += ["frontmatter: " + l for l in r.stdout.splitlines() if l.strip()]
    for f in sorted(agent_dir.glob("*.md")):
        raw = f.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            bad.append(f"agent UTF-8 BOM present: agents/{f.name}")
        text = raw.decode("utf-8", errors="replace").lstrip("\ufeff")
        m = re.match(r"---\n(.*?)\n---", text.replace("\r\n", "\n"), re.S)
        fm = dict(re.findall(r"^([\w-]+):\s*(.*)$", m.group(1), re.M)) if m else {}
        if not m:
            bad.append(f"agent frontmatter missing: agents/{f.name}")
        else:
            if fm.get("name") != f.stem:
                bad.append(f"agent name '{fm.get('name')}' does not match file: agents/{f.name}")
            if not fm.get("description", "").strip():
                bad.append(f"agent description missing: agents/{f.name}")
            if "color" in fm:
                bad.append(f"agent has Claude-only 'color:' key: agents/{f.name}")
            if fm.get("model") and fm.get("model").strip() not in VALID_MODELS:
                bad.append(f"agent model '{fm.get('model')}' not in {sorted(VALID_MODELS)}: agents/{f.name}")
        fence = False
        for n, l in enumerate(text.splitlines(), 1):
            if l.lstrip().startswith("```"):
                fence = not fence
            elif not fence and re.match(r"[\s>*\"']*(you are|act as)\b", l, re.I):
                bad.append(f"identity line: agents/{f.name}:{n}")
    nref = 0
    for f, rel in scan_files():
        nref += 1
        for n, l in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for name in REMOVED:
                if re.search(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", l) and "superseded" not in l.lower() and "removed" not in l.lower():
                    bad.append(f"removed name '{name}': {rel}:{n}")
            for m in re.finditer(r"(?<![\w/.@-])agent-[a-z][a-z-]*[a-z]", l):
                t = m.group(0)
                if t in agents or t.startswith(NOT_AGENTS):
                    continue
                bad.append(f"no such agent '{t}': {rel}:{n}")
            for m in re.finditer(r"\b(?:all )?(\d+) (?:global |kept )?agents\b", l):
                if int(m.group(1)) != len(agents):
                    bad.append(f"agent count {m.group(1)} but agents/ has {len(agents)}: {rel}:{n}")
    for b in bad:
        print(b.encode("ascii", "replace").decode())
    if bad:
        print(f"config_check: {len(bad)} problem(s)"); return 1
    print(f"config_check: ok ({len(agents)} agents, {nref} files scanned)"); return 0


if __name__ == "__main__":
    sys.exit(main())
