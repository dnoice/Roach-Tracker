#!/bin/bash

#
# File: verify.sh
# Path: verify.sh
# Purpose: Verification script to check Roach Tracker installation
# Author: dnoice + Claude AI
# Version: 1.0.0
# Created: 2025-10-31
# Updated: 2025-10-31
#

echo "========================================="
echo "  Roach Tracker - Installation Verification"
echo "========================================="
echo ""

ERRORS=0

# Check Python
echo "[1/8] Checking Python..."
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 found: $(python3 --version)"
else
    echo "✗ Python 3 not found"
    ((ERRORS++))
fi

# Check virtual environment
echo ""
echo "[2/8] Checking virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "✗ Virtual environment not found"
    ((ERRORS++))
fi

# Check .env file
echo ""
echo "[3/8] Checking .env file..."
if [ -f ".env" ]; then
    echo "✓ .env file exists"
else
    echo "✗ .env file not found"
    ((ERRORS++))
fi

# Check directory structure
echo ""
echo "[4/8] Checking directory structure..."
DIRS=("app" "templates" "static" "static/css" "static/js" "static/uploads" "data" "exports" "docs/branches")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir/"
    else
        echo "  ✗ $dir/ missing"
        ((ERRORS++))
    fi
done

# Check Python files
echo ""
echo "[5/8] Checking Python application files..."
FILES=("app/__init__.py" "app/main.py" "app/models.py" "app/utils.py")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file missing"
        ((ERRORS++))
    fi
done

# Check templates
echo ""
echo "[6/8] Checking HTML templates..."
TEMPLATES=("templates/base.html" "templates/index.html" "templates/log_sighting.html" "templates/view_sightings.html" "templates/view_sighting.html" "templates/edit_sighting.html" "templates/statistics.html")
for template in "${TEMPLATES[@]}"; do
    if [ -f "$template" ]; then
        echo "  ✓ $template"
    else
        echo "  ✗ $template missing"
        ((ERRORS++))
    fi
done

# Check static files
echo ""
echo "[7/8] Checking static files..."
STATIC=("static/css/style.css" "static/js/main.js")
for static in "${STATIC[@]}"; do
    if [ -f "$static" ]; then
        echo "  ✓ $static"
    else
        echo "  ✗ $static missing"
        ((ERRORS++))
    fi
done

# Check dependencies
echo ""
echo "[8/8] Checking Python dependencies..."
if [ -d "venv" ]; then
    source venv/bin/activate
    DEPS=("flask" "PIL" "reportlab" "dotenv")
    for dep in "${DEPS[@]}"; do
        if python3 -c "import $dep" 2>/dev/null; then
            echo "  ✓ $dep installed"
        else
            echo "  ✗ $dep not installed"
            ((ERRORS++))
        fi
    done
fi

# Summary
echo ""
echo "========================================="
if [ $ERRORS -eq 0 ]; then
    echo "  ✓ All checks passed!"
    echo "  Installation is complete and verified."
    echo ""
    echo "  Run ./run.sh to start the application"
else
    echo "  ✗ $ERRORS error(s) found"
    echo "  Please run ./setup.sh to fix issues"
fi
echo "========================================="
echo ""
