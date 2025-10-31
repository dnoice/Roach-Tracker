#!/bin/bash

#
# File: setup.sh
# Path: setup.sh
# Purpose: Initial setup script for Roach Tracker
# Author: dnoice + Claude AI
# Version: 1.0.0
# Created: 2025-10-31
# Updated: 2025-10-31
#

set -e

echo "========================================="
echo "  Roach Tracker - Initial Setup"
echo "========================================="
echo ""

# Check Python version
echo "[1/5] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "[4/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create .env file
echo ""
echo "[5/5] Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo "⚠ Please edit .env and set your SECRET_KEY"
else
    echo "✓ .env file already exists"
fi

# Initialize database
echo ""
echo "Initializing database..."
python3 -c "from app import create_app; app = create_app(); print('✓ Database initialized')"

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and set a strong SECRET_KEY"
echo "  2. Run ./run.sh to start the application"
echo "  3. Open http://localhost:5000 in your browser"
echo ""
