#!/bin/bash
# Automated Bug Bounty Toolkit Launcher
# Owner: Jashu

# Make sure virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "[!] Virtual environment not active. Activating..."
    source venv/bin/activate
fi

if [ -z "$TARGET" ]; then
    echo "[*] No TARGET specified, using targets.txt..."
    python3 main.py
else
    echo "[*] Scanning TARGET: $TARGET"
    python3 main.py "$TARGET"
fi
