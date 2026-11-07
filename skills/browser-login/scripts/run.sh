#!/bin/bash
# Starts the scenario Chrome if needed, then opens the product, signing in first when the build allows.
DIR="$(cd "$(dirname "$0")" && pwd)"
export SCENARIO_CDP_PORT="${SCENARIO_CDP_PORT:-9223}"
if [ $# -eq 0 ]; then
  echo "Usage: run.sh <build> [product]. Try run.sh preview1 list."
  exit 2
fi
if [ "$2" = "list" ]; then
  python "$DIR/login.py" "$@"
  exit $?
fi
OUT="$(python "$DIR/login.py" --url "$@" 2>/dev/null)"
RC=$?
if [ $RC -ne 0 ]; then
  echo "$OUT"
  exit $RC
fi

up() { curl -s --max-time 3 "http://127.0.0.1:${SCENARIO_CDP_PORT}/json/version" > /dev/null; }
if ! up; then
  bash "$HOME/.gemini/skills/browser-scenarios/scripts/start-chrome.sh" > /dev/null || { echo "Could not start the scenario Chrome."; exit 2; }
fi
python "$DIR/login.py" "$@" 2>&1 | grep -v -E "DeprecationWarning|trace-deprecation"
exit "${PIPESTATUS[0]}"
