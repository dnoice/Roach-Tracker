"""
File: security.py
Path: app/security.py
Purpose: Security utilities including logging, rate limiting, and audit trails
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict
from collections import defaultdict
from flask import request, current_app
import sqlite3
from contextlib import contextmanager


# Configure security logger
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)


class SecurityEvent:
    """Security event types for logging."""
    LOGIN_SUCCESS = 'login_success'
    LOGIN_FAILURE = 'login_failed'
    LOGOUT = 'logout'
    REGISTRATION = 'registration'
    PASSWORD_CHANGE = 'password_change'
    USER_CREATED = 'user_created'
    USER_DELETED = 'user_deleted'
    USER_ACTIVATED = 'user_activated'
    USER_DEACTIVATED = 'user_deactivated'
    ROLE_CHANGED = 'role_changed'
    UNAUTHORIZED_ACCESS = 'unauthorized_access'
    ACCOUNT_LOCKED = 'account_locked'


def log_security_event(event_type: str, username: str = None, user_id: int = None,
                       details: str = None, ip_address: str = None, success: bool = True):
    """
    Log a security event.

    Args:
        event_type: Type of security event (use SecurityEvent constants)
        username: Username associated with event
        user_id: User ID associated with event
        details: Additional details about the event
        ip_address: IP address of the request
        success: Whether the action was successful
    """
    # Get IP address from request if not provided
    if ip_address is None and request:
        ip_address = request.remote_addr or 'unknown'

    # Build log message
    log_parts = [
        f"[{event_type.upper()}]",
        f"IP: {ip_address}",
    ]

    if username:
        log_parts.append(f"User: {username}")
    if user_id:
        log_parts.append(f"UserID: {user_id}")
    if details:
        log_parts.append(f"Details: {details}")
    if not success:
        log_parts.append("STATUS: FAILED")

    log_message = " | ".join(log_parts)

    # Log based on severity
    if not success or event_type in (SecurityEvent.LOGIN_FAILURE, SecurityEvent.UNAUTHORIZED_ACCESS):
        security_logger.warning(log_message)
    else:
        security_logger.info(log_message)

    # Store in database audit log
    try:
        store_audit_log(event_type, username, user_id, details, ip_address, success)
    except Exception as e:
        current_app.logger.error(f"Failed to store audit log: {e}")


def store_audit_log(event_type: str, username: str = None, user_id: int = None,
                    details: str = None, ip_address: str = None, success: bool = True):
    """
    Store security event in audit log table.

    Args:
        event_type: Type of security event
        username: Username associated with event
        user_id: User ID associated with event
        details: Additional details
        ip_address: IP address
        success: Whether action was successful
    """
    db_path = current_app.config.get('DATABASE', 'data/roach_tracker.db')

    @contextmanager
    def get_connection():
        conn = sqlite3.connect(db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # Ensure audit_log table exists
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                username TEXT,
                user_id INTEGER,
                details TEXT,
                ip_address TEXT,
                success INTEGER DEFAULT 1,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert audit entry
        cursor.execute('''
            INSERT INTO audit_log (event_type, username, user_id, details, ip_address, success)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (event_type, username, user_id, details, ip_address, 1 if success else 0))


class RateLimiter:
    """
    In-memory rate limiter for authentication attempts.
    For production, use Redis or similar persistent store.
    """

    def __init__(self):
        # Store: {identifier: [(timestamp, success), ...]}
        self.attempts = defaultdict(list)
        # Store: {identifier: lockout_until_timestamp}
        self.lockouts = {}
        # Configuration
        self.max_attempts = 5
        self.window_seconds = 300  # 5 minutes
        self.lockout_duration = 900  # 15 minutes

    def _clean_old_attempts(self, identifier: str):
        """Remove attempts outside the time window."""
        cutoff = datetime.now() - timedelta(seconds=self.window_seconds)
        self.attempts[identifier] = [
            (ts, success) for ts, success in self.attempts[identifier]
            if ts > cutoff
        ]

    def is_locked_out(self, identifier: str) -> bool:
        """
        Check if identifier is currently locked out.

        Args:
            identifier: IP address or username

        Returns:
            bool: True if locked out
        """
        if identifier in self.lockouts:
            if datetime.now() < self.lockouts[identifier]:
                return True
            else:
                # Lockout expired, remove it
                del self.lockouts[identifier]
                self.attempts[identifier] = []
        return False

    def get_lockout_time_remaining(self, identifier: str) -> Optional[int]:
        """
        Get remaining lockout time in seconds.

        Args:
            identifier: IP address or username

        Returns:
            Optional[int]: Seconds remaining, or None if not locked out
        """
        if identifier in self.lockouts:
            remaining = (self.lockouts[identifier] - datetime.now()).total_seconds()
            if remaining > 0:
                return int(remaining)
            else:
                del self.lockouts[identifier]
        return None

    def record_attempt(self, identifier: str, success: bool):
        """
        Record an authentication attempt.

        Args:
            identifier: IP address or username
            success: Whether the attempt was successful
        """
        self._clean_old_attempts(identifier)

        # Record the attempt
        self.attempts[identifier].append((datetime.now(), success))

        # If successful, clear all failed attempts
        if success:
            self.attempts[identifier] = []
            if identifier in self.lockouts:
                del self.lockouts[identifier]
            return

        # Check if we should lock out
        failed_attempts = [1 for ts, success in self.attempts[identifier] if not success]
        if len(failed_attempts) >= self.max_attempts:
            self.lockouts[identifier] = datetime.now() + timedelta(seconds=self.lockout_duration)
            log_security_event(
                SecurityEvent.ACCOUNT_LOCKED,
                details=f"Account locked after {self.max_attempts} failed attempts",
                ip_address=identifier
            )

    def get_remaining_attempts(self, identifier: str) -> int:
        """
        Get number of remaining attempts before lockout.

        Args:
            identifier: IP address or username

        Returns:
            int: Number of attempts remaining
        """
        self._clean_old_attempts(identifier)
        failed_attempts = [1 for ts, success in self.attempts[identifier] if not success]
        return max(0, self.max_attempts - len(failed_attempts))


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(identifier: str) -> tuple[bool, Optional[str]]:
    """
    Check if an identifier is rate limited.

    Args:
        identifier: Username or IP address

    Returns:
        Tuple of (is_allowed, error_message)
    """
    if rate_limiter.is_locked_out(identifier):
        remaining = rate_limiter.get_lockout_time_remaining(identifier)
        minutes = remaining // 60
        seconds = remaining % 60
        if minutes > 0:
            time_str = f"{minutes} minute(s) and {seconds} second(s)"
        else:
            time_str = f"{seconds} second(s)"
        return False, f"Account temporarily locked. Try again in {time_str}."

    return True, None


def record_login_attempt(username: str, ip_address: str, success: bool):
    """
    Record a login attempt for rate limiting.

    Args:
        username: Username attempting login
        ip_address: IP address of request
        success: Whether login was successful
    """
    # Record for both username and IP
    rate_limiter.record_attempt(username.lower(), success)
    rate_limiter.record_attempt(ip_address, success)


def get_client_ip() -> str:
    """
    Get client IP address from request, handling proxies.

    Returns:
        str: Client IP address
    """
    # Check for proxy headers
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs, take the first
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr or 'unknown'

    return ip
