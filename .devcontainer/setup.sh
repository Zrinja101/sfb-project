#!/bin/bash

set -e

# Create venv
python -m venv .venv

# Activate
source .venv/bin/activate

# Install deps if present
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Dev tools (important for your project)
pip install pytest black flake8 mypy pyyaml

echo "✅ Dev container setup complete"