#!/bin/bash

# Activate the virtual environment
.venv/bin/activate

# Run the app and capture the process ID
app_pid=$(nohup python3 src/app.py 2>&1 & echo $!)

# Print the process ID
echo "Process ID: $app_pid"

# Detach from the current terminal
disown
