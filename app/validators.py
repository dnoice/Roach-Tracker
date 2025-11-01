"""
File: validators.py
Path: app/validators.py
Purpose: Input validation utilities for authentication and data security
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format with comprehensive regex.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required"

    email = email.strip()

    # RFC 5322 compliant email regex (simplified but robust)
    email_pattern = re.compile(
        r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@'
        r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
        r'(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    )

    if not email_pattern.match(email):
        return False, "Invalid email format"

    if len(email) > 254:  # RFC 5321
        return False, "Email address is too long"

    local_part, domain = email.rsplit('@', 1)
    if len(local_part) > 64:  # RFC 5321
        return False, "Email local part is too long"

    return True, ""


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username with strict rules.

    Args:
        username: Username to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username or not isinstance(username, str):
        return False, "Username is required"

    username = username.strip()

    # Length check
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 30:
        return False, "Username must be at most 30 characters"

    # Character check: alphanumeric, underscore, hyphen only
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"

    # Must start with letter or number
    if not re.match(r'^[a-zA-Z0-9]', username):
        return False, "Username must start with a letter or number"

    # Reserved names
    reserved_names = {
        'admin', 'root', 'system', 'administrator', 'moderator',
        'null', 'undefined', 'api', 'www', 'ftp', 'mail', 'support'
    }
    if username.lower() in reserved_names:
        return False, "This username is reserved"

    return True, ""


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength with comprehensive checks.

    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    - No common patterns

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"

    # Length check
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if len(password) > 128:
        return False, "Password must be at most 128 characters"

    # Character type checks
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/~`]', password))

    if not has_upper:
        return False, "Password must contain at least one uppercase letter"
    if not has_lower:
        return False, "Password must contain at least one lowercase letter"
    if not has_digit:
        return False, "Password must contain at least one number"
    if not has_special:
        return False, "Password must contain at least one special character (!@#$%^&*...)"

    # Common password patterns
    common_patterns = [
        'password', '12345678', 'qwerty', 'abc123', 'letmein',
        'welcome', 'monkey', '1234567890', 'password123'
    ]
    password_lower = password.lower()
    for pattern in common_patterns:
        if pattern in password_lower:
            return False, "Password contains a common pattern. Please choose a stronger password"

    # Sequential characters check
    if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
        return False, "Password should not contain sequential numbers"

    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        return False, "Password should not contain sequential letters"

    # Repeated characters
    if re.search(r'(.)\1{2,}', password):
        return False, "Password should not contain repeated characters (e.g., 'aaa')"

    return True, ""


def get_password_strength_score(password: str) -> int:
    """
    Calculate password strength score (0-100).

    Args:
        password: Password to score

    Returns:
        int: Strength score from 0 to 100
    """
    if not password:
        return 0

    score = 0

    # Length scoring (max 30 points)
    length = len(password)
    if length >= 8:
        score += 10
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10

    # Character variety (max 40 points)
    if re.search(r'[a-z]', password):
        score += 10
    if re.search(r'[A-Z]', password):
        score += 10
    if re.search(r'\d', password):
        score += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/~`]', password):
        score += 10

    # Complexity bonus (max 30 points)
    unique_chars = len(set(password))
    if unique_chars >= 8:
        score += 10
    if unique_chars >= 12:
        score += 10
    if unique_chars >= 16:
        score += 10

    return min(score, 100)


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input by removing potentially dangerous characters.

    Args:
        text: Text to sanitize
        max_length: Maximum allowed length

    Returns:
        str: Sanitized text
    """
    if not text or not isinstance(text, str):
        return ""

    # Strip whitespace
    text = text.strip()

    # Truncate to max length
    text = text[:max_length]

    # Remove null bytes
    text = text.replace('\x00', '')

    # Remove other control characters except newline and tab
    text = ''.join(char for char in text if char == '\n' or char == '\t' or not (0 <= ord(char) < 32))

    return text


def validate_full_name(full_name: str) -> Tuple[bool, str]:
    """
    Validate full name.

    Args:
        full_name: Full name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not full_name:
        return True, ""  # Optional field

    if not isinstance(full_name, str):
        return False, "Full name must be text"

    full_name = full_name.strip()

    if len(full_name) < 2:
        return False, "Full name must be at least 2 characters"

    if len(full_name) > 100:
        return False, "Full name must be at most 100 characters"

    # Only letters, spaces, hyphens, apostrophes
    if not re.match(r'^[a-zA-Z\s\-\'\.]+$', full_name):
        return False, "Full name can only contain letters, spaces, hyphens, and apostrophes"

    return True, ""
