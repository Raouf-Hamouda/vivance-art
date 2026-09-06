#!/bin/zsh
cd "$(dirname "$0")"
if ! lsof -iTCP:8774 -sTCP:LISTEN >/dev/null 2>&1; then nohup python3 serve.py 8774 >/dev/null 2>&1 & sleep 1; fi
open "http://localhost:8774/"
