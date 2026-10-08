#!/usr/bin/env bash

set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/launcher.log"
VENV_ACTIVATE="$SCRIPT_DIR/../venv/bin/activate"

cd "$SCRIPT_DIR" || exit 1

if [ ! -f "$VENV_ACTIVATE" ]; then
	printf 'Expected virtual environment activation script not found: %s\n' "$VENV_ACTIVATE" | tee "$LOG_FILE"
	exit 1
fi

source "$VENV_ACTIVATE"

printf 'Python: %s\nScript: %s/integrated_main3.py\nWorking directory: %s\n\n' "$(command -v python)" "$SCRIPT_DIR" "$SCRIPT_DIR" >"$LOG_FILE"
python "$SCRIPT_DIR/integrated_main3.py" >>"$LOG_FILE" 2>&1
EXIT_CODE=$?

if [ "$EXIT_CODE" -ne 0 ]; then
	printf '\nThe application stopped with exit code %s. Details: %s\n' "$EXIT_CODE" "$LOG_FILE" >>"$LOG_FILE"
fi

exit "$EXIT_CODE"
