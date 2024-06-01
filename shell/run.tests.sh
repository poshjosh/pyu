#!/usr/bin/env bash

WORKING_DIR="src"

cd .. && source .venv/bin/activate || exit 1

export PYTHONUNBUFFERED=1

cd "$WORKING_DIR" || (printf "\nCould not change to working dir: %s\n" "$WORKING_DIR" && exit 1)

printf "\nWorking from: %s\n" "$(pwd)"

printf "\nStarting tests\n\n"

python3 -m unittest discover -s test/io -p "*_test.py"