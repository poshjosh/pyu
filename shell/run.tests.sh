#!/usr/bin/env bash

cd .. && source .venv/bin/activate || exit 1

printf "\nWorking from: %s\n" "$(pwd)"

printf "\nExporting environment\n"

export PYTHONUNBUFFERED=1

printf "\nStarting tests\n\n"

python3 -m unittest discover -s test/pyu -p "*_test.py"
