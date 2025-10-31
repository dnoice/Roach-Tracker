#!/usr/bin/env python3
"""
File: create_admin.py
Path: create_admin.py
Purpose: Create initial administrator user for Roach Tracker
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31

Usage:
    python create_admin.py
"""

import os
import sys
import getpass
from dotenv import load_dotenv

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from app.models import Database


def create_admin_user():
    """Create an administrator user interactively."""
    print("=" * 60)
    print("Roach Tracker - Admin User Setup")
    print("=" * 60)
    print()

    # Initialize database
    db_path = os.getenv('DATABASE_PATH', 'data/roach_tracker.db')
    db = Database(db_path)

    print(f"Database: {db_path}")
    print()

    # Check if admin users already exist
    try:
        admins = db.get_all_users(role='admin')
        if admins:
            print(f"WARNING: {len(admins)} admin user(s) already exist:")
            for admin in admins:
                print(f"  - {admin['username']} ({admin['email']})")
            print()
            confirm = input("Create another admin user? (yes/no): ").strip().lower()
            if confirm not in ('yes', 'y'):
                print("Aborted.")
                return
            print()
    except Exception as e:
        print(f"Error checking existing admins: {e}")
        print("Continuing anyway...")
        print()

    # Gather user information
    print("Enter admin user details:")
    print("-" * 60)

    while True:
        username = input("Username (min 3 chars): ").strip()
        if len(username) >= 3:
            break
        print("ERROR: Username must be at least 3 characters")

    while True:
        email = input("Email address: ").strip()
        if '@' in email and '.' in email:
            break
        print("ERROR: Please enter a valid email address")

    full_name = input("Full name (optional): ").strip()

    while True:
        password = getpass.getpass("Password (min 8 chars): ")
        if len(password) >= 8:
            password_confirm = getpass.getpass("Confirm password: ")
            if password == password_confirm:
                break
            print("ERROR: Passwords do not match")
        else:
            print("ERROR: Password must be at least 8 characters")

    print()
    print("-" * 60)
    print("User Details:")
    print(f"  Username:  {username}")
    print(f"  Email:     {email}")
    print(f"  Full Name: {full_name or '(none)'}")
    print(f"  Role:      admin")
    print("-" * 60)

    confirm = input("\nCreate this admin user? (yes/no): ").strip().lower()
    if confirm not in ('yes', 'y'):
        print("Aborted.")
        return

    # Create user
    try:
        user_id = db.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
            full_name=full_name if full_name else None
        )

        print()
        print("=" * 60)
        print(f"SUCCESS: Admin user created!")
        print(f"User ID: {user_id}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print("=" * 60)
        print()
        print("You can now log in at: http://localhost:5000/login")
        print()

    except ValueError as e:
        print()
        print("=" * 60)
        print(f"ERROR: {e}")
        print("=" * 60)
        sys.exit(1)
    except Exception as e:
        print()
        print("=" * 60)
        print(f"ERROR: An unexpected error occurred: {e}")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    try:
        create_admin_user()
    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(1)
