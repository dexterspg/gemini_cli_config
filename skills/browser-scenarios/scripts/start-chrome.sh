#!/bin/bash
# Start the scenario Chrome: its own profile, debugging port ${SCENARIO_CDP_PORT:-9223} on this machine only. Leave it open.
# Windows + Git Bash, Chrome in Program Files. Usage: bash start-chrome.sh [url]
PROFILE="$HOME/.gemini/browser-profile"
CDP_PORT="${SCENARIO_CDP_PORT:-9223}"
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
mkdir -p "$PROFILE"
up() { curl -s --max-time 3 "http://127.0.0.1:${CDP_PORT}/json/version" > /dev/null; }

if up; then
  echo "Something already answers on port ${CDP_PORT}; assuming it is the scenario Chrome."
  exit 0
fi
[ -x "$CHROME" ] || { echo "Chrome not found at $CHROME"; exit 1; }

"$CHROME" \
  --remote-debugging-port="${CDP_PORT}" \
  --user-data-dir="$(cygpath -w "$PROFILE")" \
  --no-first-run --no-default-browser-check \
  "${1:-about:blank}" < /dev/null > /dev/null 2>&1 &
disown

for _ in $(seq 1 15); do
  up && { echo "Scenario Chrome is up. Open a build with browser-login."; exit 0; }
  sleep 1
done
echo "Chrome did not open the debugging port. If this profile is already open in a Chrome started without the port, close that window and run again."
exit 1
