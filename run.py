#!/usr/bin/env python3
"""
File: run.py
Path: run.py
Purpose: Application entry point for Roach Tracker
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31

Usage:
    python run.py
    python run.py --host 0.0.0.0 --port 5000
    python run.py --debug
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Roach Tracker - Pest Documentation System')
    parser.add_argument('--host', default=os.getenv('HOST', '0.0.0.0'),
                       help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=int(os.getenv('PORT', 5000)),
                       help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true',
                       default=os.getenv('FLASK_ENV') == 'development',
                       help='Enable debug mode')
    parser.add_argument('--no-debug', action='store_true',
                       help='Disable debug mode (overrides --debug)')

    args = parser.parse_args()

    # Import app after argument parsing
    try:
        from app import create_app
    except ImportError as e:
        print(f"Error importing app module: {e}")
        print("\nMake sure you're running from the project root directory.")
        print("If you haven't set up the project yet, run: ./setup.sh")
        sys.exit(1)

    # Create the Flask application
    app = create_app()

    # Determine debug mode
    debug = args.debug and not args.no_debug

    # Print startup information
    print("=" * 60)
    print("  Roach Tracker - Secure Pest Documentation System")
    print("=" * 60)
    print(f"\n  Version: 1.2.0")
    print(f"  URL: http://{args.host}:{args.port}")
    print(f"  Debug Mode: {'ON' if debug else 'OFF'}")
    print(f"\n  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Run the application
    try:
        app.run(host=args.host, port=args.port, debug=debug)
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
