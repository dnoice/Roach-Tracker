"""
File: auth.py
Path: app/auth.py
Purpose: Authentication utilities and role-based access control
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31
"""

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


def login_required_with_role(*allowed_roles):
    """
    Decorator to require login and specific role(s).

    Args:
        *allowed_roles: Variable number of role strings

    Usage:
        @login_required_with_role('admin')
        @login_required_with_role('admin', 'property_manager')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'info')
                return redirect(url_for('login'))

            # Check if user has required role
            if allowed_roles and current_user.role not in allowed_roles:
                flash('You do not have permission to access this page.', 'error')
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorator to require admin role.

    Usage:
        @admin_required
        def admin_only_view():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('login'))

        if not current_user.is_admin():
            flash('Administrator access required.', 'error')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def property_manager_required(f):
    """
    Decorator to require property manager or admin role.

    Usage:
        @property_manager_required
        def manager_view():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('login'))

        if not (current_user.is_property_manager() or current_user.is_admin()):
            flash('Property manager access required.', 'error')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def check_property_access(user_id, property_id):
    """
    Check if a user has access to a specific property.

    Args:
        user_id: User ID to check
        property_id: Property ID to check access for

    Returns:
        bool: True if user has access, False otherwise
    """
    from flask import current_app
    from app.models import Database

    # Admin has access to all properties
    if current_user.is_authenticated and current_user.is_admin():
        return True

    # Check if user is associated with the property
    db = Database(current_app.config['DATABASE'])
    try:
        user_properties = db.get_user_properties(user_id)
        return any(prop['id'] == property_id for prop in user_properties)
    except ValueError:
        return False


def get_user_accessible_properties(user_id):
    """
    Get all properties accessible by a user.

    Args:
        user_id: User ID

    Returns:
        List[Dict]: List of accessible properties
    """
    from flask import current_app
    from app.models import Database

    db = Database(current_app.config['DATABASE'])

    # Admin can access all properties
    if current_user.is_authenticated and current_user.is_admin():
        return db.get_all_properties()

    # Regular users can only access their assigned properties
    try:
        return db.get_user_properties(user_id)
    except ValueError:
        return []
