#!/usr/bin/env python3
"""
File: check_setup.py
Path: check_setup.py
Purpose: Verify that the Roach Tracker environment is properly configured
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31
"""

import os
import sys


def check_venv():
    """Check if virtual environment exists."""
    if os.path.exists('venv'):
        print("✓ Virtual environment exists")
        return True
    else:
        print("✗ Virtual environment not found")
        print("  Run: ./setup.sh")
        return False


def check_env_file():
    """Check if .env file exists."""
    if os.path.exists('.env'):
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file not found")
        print("  Run: ./setup.sh")
        return False


def check_database():
    """Check if database exists."""
    db_path = os.getenv('DATABASE_PATH', 'data/roach_tracker.db')
    if os.path.exists(db_path):
        print(f"✓ Database exists: {db_path}")
        return True
    else:
        print(f"✗ Database not found: {db_path}")
        print("  Database will be created on first run")
        return True  # Not critical


def check_imports():
    """Check if required modules can be imported."""
    try:
        import flask
        print(f"✓ Flask installed (version {flask.__version__})")
    except ImportError:
        print("✗ Flask not installed")
        print("  Run: ./setup.sh")
        return False

    try:
        import flask_login
        print("✓ Flask-Login installed")
    except ImportError:
        print("✗ Flask-Login not installed")
        print("  Run: ./setup.sh")
        return False

    try:
        from PIL import Image
        print("✓ Pillow installed")
    except ImportError:
        print("✗ Pillow not installed")
        print("  Run: ./setup.sh")
        return False

    try:
        import reportlab
        print("✓ ReportLab installed")
    except ImportError:
        print("✗ ReportLab not installed")
        print("  Run: ./setup.sh")
        return False

    return True


def check_app_structure():
    """Check if app module can be imported."""
    try:
        from app import create_app
        print("✓ App module can be imported")
        return True
    except ImportError as e:
        print(f"✗ App module import failed: {e}")
        return False


def main():
    """Run all checks."""
    print()
    print("=" * 60)
    print("  Roach Tracker - Environment Check")
    print("=" * 60)
    print()

    # Check if we're in the right directory
    if not os.path.exists('app') or not os.path.exists('setup.sh'):
        print("✗ Not in Roach-Tracker root directory")
        print("  Please run this script from the project root")
        print()
        sys.exit(1)

    checks = [
        ("Virtual Environment", check_venv),
        ("Environment File", check_env_file),
        ("Database", check_database),
        ("Python Modules", check_imports),
        ("App Structure", check_app_structure),
    ]

    all_passed = True
    for name, check_func in checks:
        print(f"\nChecking {name}:")
        if not check_func():
            all_passed = False

    print()
    print("=" * 60)
    if all_passed:
        print("  ✓ All checks passed!")
        print()
        print("  You can now run the application:")
        print("    ./run.sh")
        print("    or")
        print("    python run.py")
    else:
        print("  ✗ Some checks failed")
        print()
        print("  Please run setup first:")
        print("    ./setup.sh")
    print("=" * 60)
    print()

    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
