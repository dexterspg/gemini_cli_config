---
name: desktop-app-storage
description: 'Use when building a desktop application that needs to persist user data (config, history, logs) across installs, updates, or .exe replacements — especially PyInstaller apps on Windows where storage location affects admin rights and data survival'
---

# Desktop App Storage

## Core Principle

**Install directory ≠ data directory.** User data must live in a user-owned path that survives reinstalls, updates, and `.exe` replacements. Never write user data next to the `.exe`.

## The Two Paths and When to Use Each

| Path | Use for | Syncs? | Admin? |
|------|---------|--------|--------|
| `%LOCALAPPDATA%\AppName\` | Config, history, temp — single-user desktop tools | No | No |
| `%APPDATA%\AppName\` (Roaming) | Config that should follow domain-joined users across machines | Yes | No |

**Default: use `%LOCALAPPDATA%` for everything.** Roaming only if the app is deployed in an enterprise domain environment where users roam between machines.

## Directory Structure

```
%LOCALAPPDATA%\AppName\
  config\        → JSON config files (survives reinstall)
  history\       → History/audit log files (survives reinstall)
  uploads\       → Temp files (auto-cleaned, never persisted)
```

## What Survives a Reinstall

| Location | Survives? |
|----------|-----------|
| `%LOCALAPPDATA%\AppName\` | ✅ Always — installers don't touch it |
| Install dir (`Program Files`, app folder) | ❌ Replaced on update |
| Next to the `.exe` | ❌ Replaced on update, also breaks PyInstaller |

## Python Implementation (PyInstaller + dev mode)

```python
import os
import sys
from pathlib import Path

APP_NAME = "MyApp"

def get_app_data_dir() -> Path:
    """
    Resolve the user data directory at runtime.

    Desktop (.exe):  %LOCALAPPDATA%\AppName\
    Dev (script):    <backend_dir>\  (convenient for local testing)

    %LOCALAPPDATA% resolves via env var — no sys.frozen check needed.
    """
    if getattr(sys, "frozen", False):
        # Running as PyInstaller .exe
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            base = Path(local_app_data) / APP_NAME
        else:
            # Fallback for non-Windows or missing env var
            base = Path.home() / ".local" / "share" / APP_NAME
    else:
        # Dev mode — store alongside the script for easy inspection
        base = Path(__file__).parent

    base.mkdir(parents=True, exist_ok=True)
    return base


def get_subdirs() -> dict:
    base = get_app_data_dir()
    dirs = {
        "config":  base / "config",
        "history": base / "history",
        "uploads": base / "uploads",
    }
    for d in dirs.values():
        d.mkdir(exist_ok=True)
    return dirs
```

## PyInstaller: Bundled Assets vs User Data

These are different problems:

```python
# Bundled read-only assets (templates, static files packed inside .exe)
def get_bundle_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)   # PyInstaller extraction temp dir
    return Path(__file__).parent

# User data (config, history) — use get_app_data_dir() above, NOT _MEIPASS
# _MEIPASS is a temp path that changes every launch — never store user data there
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Store config next to `.exe` | Lost on every update | Use `%LOCALAPPDATA%` |
| Store config in `sys._MEIPASS` | Path changes every launch | Use `%LOCALAPPDATA%` |
| Use `%APPDATA%` (Roaming) for single-user tool | Unnecessary sync, bloats roaming profiles | Use `%LOCALAPPDATA%` |
| Write to `Program Files` | Requires admin rights | Use `%LOCALAPPDATA%` |
| No fallback for missing `LOCALAPPDATA` | Crashes on non-Windows | Add `Path.home()` fallback |

## Cross-Platform Equivalents

| OS | User data path |
|----|---------------|
| Windows | `%LOCALAPPDATA%\AppName\` |
| macOS | `~/Library/Application Support/AppName/` |
| Linux | `~/.local/share/AppName/` or `$XDG_DATA_HOME/AppName/` |

---

## Building the .exe (PyInstaller + FastAPI + Vue)

### Stack assumptions
- Backend: FastAPI + uvicorn + pandas + openpyxl + sqlite3
- Frontend: Vue 3 built with Vite → `frontend-dist/`
- Build script lives in `webapp/`, PyInstaller runs from `webapp/backend/`

### Build script pattern

```python
# Run from webapp/
# Step 1: build frontend
subprocess.run(["npm", "run", "build"], cwd="frontend-vue/")
# Output lands in frontend-dist/ (configured in vite.config.js outDir)

# Step 2: PyInstaller from backend/
subprocess.run([sys.executable, "-m", "PyInstaller", ...], cwd="backend/")

# Step 3: zip dist/AppName/ — use a flat structure to avoid double-nesting
```

### PyInstaller command template

```python
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onedir",
    "--console",                    # use --noconsole only after confirming it starts
    f"--name={APP_NAME}",
    # Bundle frontend dist (src relative to cwd=backend/, dst inside _internal/)
    f"--add-data=../frontend-dist{os.pathsep}frontend-dist",
    f"--add-data=services{os.pathsep}services",
    f"--add-data=models{os.pathsep}models",
    # uvicorn internals (commonly missed by PyInstaller)
    "--hidden-import=uvicorn.logging",
    "--hidden-import=uvicorn.loops",
    "--hidden-import=uvicorn.loops.auto",
    "--hidden-import=uvicorn.loops.asyncio",
    "--hidden-import=uvicorn.protocols",
    "--hidden-import=uvicorn.protocols.http.auto",
    "--hidden-import=uvicorn.protocols.http.h11_impl",
    "--hidden-import=uvicorn.protocols.websockets.auto",
    "--hidden-import=uvicorn.lifespan.on",
    "--hidden-import=uvicorn.lifespan.off",
    # file uploads
    "--hidden-import=multipart",
    "--hidden-import=python_multipart",
    # pydantic v2
    "--hidden-import=pydantic",
    "--hidden-import=pydantic_core",
    # pandas internals
    "--hidden-import=pandas._libs.tslibs.np_datetime",
    "--hidden-import=pandas._libs.tslibs.nattype",
    "--hidden-import=pandas._libs.tslibs.timedeltas",
    "--hidden-import=pandas._libs.tslibs.offsets",
    # collect-all for packages with dynamic imports
    "--collect-all=uvicorn",
    "--collect-all=fastapi",
    "--collect-all=starlette",
    "--collect-all=pydantic",
    "--collect-all=openpyxl",
    "--noconfirm",
    "--clean",
    "app.py",
]
```

### Accessing bundled frontend at runtime

```python
def get_frontend_path() -> Path:
    if getattr(sys, "frozen", False):
        # PyInstaller onedir: _internal/ is next to the .exe
        return Path(sys.executable).parent / "_internal" / "frontend-dist"
    return Path(__file__).parent.parent / "frontend-dist"
```

### --console vs --noconsole

| Flag | When to use |
|------|-------------|
| `--console` | Always during development — shows Python errors on startup |
| `--noconsole` | Release only — after confirming the exe starts cleanly with `--console` |

**Never ship `--noconsole` without first verifying `--console` works.** Silent crashes are impossible to debug without the console.

### Zip packaging — avoid double-nesting

```python
# WRONG: zip contains AppName_v1.0.0/AppName_v1.0.0/AppName/...
with zipfile.ZipFile(zip_path, "w") as zf:
    for file in dist_dir.rglob("*"):
        arcname = Path(PACKAGE_NAME) / file.relative_to(dist_dir.parent)
        zf.write(file, arcname)

# CORRECT: zip contains AppName_v1.0.0/AppName/...
with zipfile.ZipFile(zip_path, "w") as zf:
    for file in dist_dir.rglob("*"):
        arcname = Path(PACKAGE_NAME) / file.relative_to(dist_dir)
        zf.write(file, arcname)
```

The fix: use `file.relative_to(dist_dir)` not `file.relative_to(dist_dir.parent)`.

### Desktop mode auto-detection

The app should auto-detect it is frozen and run in desktop mode — no need to pass `--desktop` as a PyInstaller argument (PyInstaller does not support passing arguments to the app that way):

```python
def main():
    is_executable = getattr(sys, "frozen", False)
    if args.desktop or is_executable:
        run_desktop_mode()   # opens browser, binds to localhost:5001
    else:
        run_web_mode()       # binds to 0.0.0.0:8000
```
