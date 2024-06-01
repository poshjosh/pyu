#!/usr/bin/env bash

set -euo pipefail

cd ..

printf "\nActivating virtual environment\n"
source .venv/bin/activate

printf "\nInstalling module for local development: %s\n" "$(pwd)"
# Make main modules accessible to test modules

python3 -m pip install -e .
