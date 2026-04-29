#!/bin/bash

# ── Quantium CI Test Runner ───────────────────────────────────────────────────
# Activates the virtual environment, runs the Dash test suite via pytest,
# and returns exit code 0 (all passed) or 1 (something went wrong).

set -e  # exit immediately on unexpected errors

# ── 1. Locate the repo root (folder this script lives in) ────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── 2. Activate the virtual environment ──────────────────────────────────────
VENV_PATH="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_PATH" ]; then
  echo "[ERROR] Virtual environment not found at: $VENV_PATH"
  echo "        Please create it with: python3.9 -m venv venv"
  exit 1
fi

echo "[INFO]  Activating virtual environment..."

# Support both Unix/macOS and Windows (Git Bash)
if [ -f "$VENV_PATH/bin/activate" ]; then
  source "$VENV_PATH/bin/activate"
elif [ -f "$VENV_PATH/Scripts/activate" ]; then
  source "$VENV_PATH/Scripts/activate"
else
  echo "[ERROR] Could not find activate script in venv."
  exit 1
fi

echo "[INFO]  Python: $(which python)"
echo "[INFO]  Python version: $(python --version)"

# ── 3. Run the test suite ─────────────────────────────────────────────────────
echo ""
echo "[INFO]  Running test suite..."
echo "────────────────────────────────────────"

pytest test_app.py -v
TEST_EXIT_CODE=$?

echo "────────────────────────────────────────"

# ── 4. Return correct exit code ───────────────────────────────────────────────
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "[PASS]  All tests passed. Exiting with code 0."
  exit 0
else
  echo "[FAIL]  One or more tests failed. Exiting with code 1."
  exit 1
fi
