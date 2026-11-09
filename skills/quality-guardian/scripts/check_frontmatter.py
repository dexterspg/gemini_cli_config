"""Frontmatter checker for ~/.gemini skills. Args: files or dirs (dirs: SKILL.md).
Prints one ASCII line per problem; exit 1 on any problem, 2 if not checked."""
import sys, pathlib
try:
    import yaml
except ImportError:
    print("NOT CHECKED: PyYAML missing"); sys.exit(2)
K = set("name paths description when_to_use argument-hint arguments disable-model-invocation user-invocable "
        "allowed-tools disallowed-tools model effort context agent background hooks shell metadata license "
        "compatibility".split())
def files(a):
    p = pathlib.Path(a)
    if p.is_file(): yield p
    elif p.is_dir():
        yield from p.rglob("SKILL.md")
bad = 0
def out(p, m):
    global bad; bad = 1; print(ascii(f"{p.as_posix()}: {m}")[1:-1])
for a in sys.argv[1:]:
    for p in files(a):
        if "synced" in p.parts: continue
        raw = p.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            out(p, "UTF-8 BOM present (causes YAML frontmatter failure)")
        t = raw.decode("utf-8", errors="replace").lstrip("\ufeff").replace("\r\n", "\n")
        if not t.startswith("---\n"):
            out(p, "frontmatter not on line 1")
            continue
        end = t.find("\n---\n", 3)
        if end < 0: out(p, "no closing ---"); continue
        try: d = yaml.safe_load(t[4:end]) or {}
        except yaml.YAMLError as e: out(p, "YAML does not parse: " + str(e).splitlines()[0]); continue
        if not isinstance(d, dict): out(p, "frontmatter is not a mapping"); continue
        extra = sorted(set(d) - K)
        if extra: out(p, f"ignored keys {extra}")
        n = len(str(d.get("description") or "")) + len(str(d.get("when_to_use") or ""))
        if n > 1536: out(p, f"description+when_to_use {n} chars > 1536")
        if len(str(d.get("description") or "")) > 1024: out(p, "description > 1024")
sys.exit(bad)
