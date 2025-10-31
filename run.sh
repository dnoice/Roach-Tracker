#!/bin/bash

#
# File: run.sh
# Path: run.sh
# Purpose: Launch script for Roach Tracker application
# Author: dnoice + Claude AI
# Version: 1.0.0
# Created: 2025-10-31
# Updated: 2025-10-31
#

set -e

echo "========================================="
echo "  Roach Tracker - Starting Application"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "✗ Virtual environment not found."
    echo "  Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "✗ .env file not found."
    echo "  Please run ./setup.sh first"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Set defaults if not specified
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}

echo "✓ Configuration loaded"
echo ""
echo "Starting Roach Tracker..."
echo "  URL: http://localhost:$PORT"
echo "  Press Ctrl+C to stop"
echo ""

# Run the Flask application
python3 -c "
from app import create_app
app = create_app()
app.run(host='$HOST', port=$PORT, debug=True)
"
