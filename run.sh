#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Run the app in the background
nohup python3 src/app.py 2>&1 &

# Deactivate the virtual environment
deactivate
