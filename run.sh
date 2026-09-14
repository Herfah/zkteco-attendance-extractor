#!/bin/bash

# Quick launch script for ZKTeco Attendance Extractor
# This makes it easy to run the app from terminal

SCRIPT_DIR=\"\$( cd \"\$( dirname \"\${BASH_SOURCE[0]}\" )\" && pwd )\"
cd \"$SCRIPT_DIR\"

if [ ! -d \"venv\" ]; then
    echo \"❌ Application not installed. Run: bash install.sh\"
    exit 1
fi

source venv/bin/activate
python main.py
