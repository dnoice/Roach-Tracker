"""
File: models.py
Path: app/models.py
Purpose: Database schema and operations for roach sighting tracking
Author: dnoice + Claude AI
Version: 1.1.0
Created: 2025-10-31
Updated: 2025-10-31
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from contextlib import contextmanager
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    """
    SQLite database manager for Roach Tracker.
    Handles all CRUD operations and schema management.
    """

    def __init__(self, db_path: str):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.

        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_database(self):
        """
        Initialize database schema if not exists.
        Creates all required tables for the application.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'resident',
                    full_name TEXT,
                    is_active INTEGER DEFAULT 1,
                    last_login TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    CHECK (role IN ('admin', 'resident', 'property_manager'))
                )
            ''')

            # Properties table for multi-tenant support
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT,
                    created_by INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            ''')

            # User-Property relationship table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_properties (
                    user_id INTEGER NOT NULL,
                    property_id INTEGER NOT NULL,
                    relationship_type TEXT NOT NULL DEFAULT 'resident',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, property_id),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
                    CHECK (relationship_type IN ('owner', 'manager', 'resident'))
                )
            ''')

            # Check if sightings table exists and if it has user_id column
            cursor.execute("PRAGMA table_info(sightings)")
            columns = [row[1] for row in cursor.fetchall()]

            if 'sightings' not in [table[0] for table in cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()]:
                # Create new sightings table with user/property support
                cursor.execute('''
                    CREATE TABLE sightings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        location TEXT NOT NULL,
                        room_type TEXT,
                        roach_count INTEGER DEFAULT 1,
                        roach_size TEXT,
                        roach_type TEXT,
                        photo_path TEXT,
                        notes TEXT,
                        weather TEXT,
                        temperature REAL,
                        time_of_day TEXT,
                        user_id INTEGER,
                        property_id INTEGER,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                        FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL
                    )
                ''')
            elif 'user_id' not in columns:
                # Migrate existing sightings table
                cursor.execute('ALTER TABLE sightings ADD COLUMN user_id INTEGER')
                cursor.execute('ALTER TABLE sightings ADD COLUMN property_id INTEGER')

    def create_sighting(self, data: Dict) -> int:
        """
        Create a new roach sighting record.

        Args:
            data: Dictionary containing sighting information

        Returns:
            int: ID of newly created sighting

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Validate required fields
        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary")
        if 'location' not in data or not data['location']:
            raise ValueError("Location is required")

        # Validate roach_count if provided
        roach_count = data.get('roach_count', 1)
        if not isinstance(roach_count, int) or roach_count < 1:
            raise ValueError("Roach count must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sightings (
                    timestamp, location, room_type, roach_count,
                    roach_size, roach_type, photo_path, notes,
                    weather, temperature, time_of_day, user_id, property_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('timestamp', datetime.now().isoformat()),
                data['location'].strip(),
                data.get('room_type'),
                roach_count,
                data.get('roach_size'),
                data.get('roach_type'),
                data.get('photo_path'),
                data.get('notes'),
                data.get('weather'),
                data.get('temperature'),
                data.get('time_of_day'),
                data.get('user_id'),
                data.get('property_id')
            ))
            return cursor.lastrowid

    def get_sighting(self, sighting_id: int) -> Optional[Dict]:
        """
        Retrieve a single sighting by ID.

        Args:
            sighting_id: ID of the sighting

        Returns:
            Dict or None: Sighting data as dictionary

        Raises:
            ValueError: If sighting_id is invalid
        """
        if not isinstance(sighting_id, int) or sighting_id < 1:
            raise ValueError("Sighting ID must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sightings WHERE id = ?', (sighting_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_sightings(self, limit: Optional[int] = None,
                          offset: int = 0) -> List[Dict]:
        """
        Retrieve all sightings with optional pagination.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List[Dict]: List of sighting records

        Raises:
            ValueError: If limit or offset are invalid
        """
        # Validate pagination parameters
        if limit is not None and (not isinstance(limit, int) or limit < 1):
            raise ValueError("Limit must be a positive integer")
        if not isinstance(offset, int) or offset < 0:
            raise ValueError("Offset must be a non-negative integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM sightings ORDER BY timestamp DESC'
            params = []
            if limit:
                query += ' LIMIT ? OFFSET ?'
                params = [limit, offset]
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def update_sighting(self, sighting_id: int, data: Dict) -> bool:
        """
        Update an existing sighting record.

        Args:
            sighting_id: ID of the sighting to update
            data: Dictionary containing updated fields

        Returns:
            bool: True if update successful

        Raises:
            ValueError: If sighting_id or data are invalid
        """
        # Validate inputs
        if not isinstance(sighting_id, int) or sighting_id < 1:
            raise ValueError("Sighting ID must be a positive integer")
        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary")
        if 'location' not in data or not data['location']:
            raise ValueError("Location is required")

        # Validate roach_count if provided
        roach_count = data.get('roach_count', 1)
        if not isinstance(roach_count, int) or roach_count < 1:
            raise ValueError("Roach count must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE sightings SET
                    timestamp = ?,
                    location = ?,
                    room_type = ?,
                    roach_count = ?,
                    roach_size = ?,
                    roach_type = ?,
                    photo_path = ?,
                    notes = ?,
                    weather = ?,
                    temperature = ?,
                    time_of_day = ?,
                    user_id = ?,
                    property_id = ?,
                    updated_at = ?
                WHERE id = ?
            ''', (
                data.get('timestamp'),
                data['location'].strip(),
                data.get('room_type'),
                roach_count,
                data.get('roach_size'),
                data.get('roach_type'),
                data.get('photo_path'),
                data.get('notes'),
                data.get('weather'),
                data.get('temperature'),
                data.get('time_of_day'),
                data.get('user_id'),
                data.get('property_id'),
                datetime.now().isoformat(),
                sighting_id
            ))
            return cursor.rowcount > 0

    def delete_sighting(self, sighting_id: int) -> bool:
        """
        Delete a sighting record.

        Args:
            sighting_id: ID of the sighting to delete

        Returns:
            bool: True if deletion successful

        Raises:
            ValueError: If sighting_id is invalid
        """
        if not isinstance(sighting_id, int) or sighting_id < 1:
            raise ValueError("Sighting ID must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sightings WHERE id = ?', (sighting_id,))
            return cursor.rowcount > 0

    def get_statistics(self) -> Dict:
        """
        Calculate comprehensive statistics from all sightings.

        Returns:
            Dict: Statistics including counts, distributions, and trends
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total sightings
            cursor.execute('SELECT COUNT(*) as total FROM sightings')
            total = cursor.fetchone()['total']

            # Total roaches
            cursor.execute('SELECT IFNULL(SUM(roach_count), 0) as total FROM sightings')
            total_roaches = cursor.fetchone()['total']

            # Location distribution
            cursor.execute('''
                SELECT location, COUNT(*) as count
                FROM sightings
                GROUP BY location
                ORDER BY count DESC
            ''')
            locations = [dict(row) for row in cursor.fetchall()]

            # Size distribution
            cursor.execute('''
                SELECT roach_size, COUNT(*) as count
                FROM sightings
                WHERE roach_size IS NOT NULL
                GROUP BY roach_size
                ORDER BY count DESC
            ''')
            sizes = [dict(row) for row in cursor.fetchall()]

            # Time of day distribution
            cursor.execute('''
                SELECT time_of_day, COUNT(*) as count
                FROM sightings
                WHERE time_of_day IS NOT NULL
                GROUP BY time_of_day
                ORDER BY count DESC
            ''')
            times = [dict(row) for row in cursor.fetchall()]

            # Recent sightings (last 7 days trend)
            cursor.execute('''
                SELECT DATE(timestamp) as date, COUNT(*) as count
                FROM sightings
                WHERE timestamp >= date('now', '-7 days')
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
            ''')
            recent_trend = [dict(row) for row in cursor.fetchall()]

            return {
                'total_sightings': total,
                'total_roaches': total_roaches,
                'locations': locations,
                'sizes': sizes,
                'times_of_day': times,
                'recent_trend': recent_trend
            }

    def search_sightings(self, query: str) -> List[Dict]:
        """
        Search sightings by location or notes.

        Args:
            query: Search query string

        Returns:
            List[Dict]: Matching sighting records

        Raises:
            ValueError: If query is invalid
        """
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

        # Sanitize query by escaping SQL wildcards to prevent wildcard injection
        # User can still use wildcards, but they must be explicit in their input
        sanitized_query = query.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        search_pattern = f'%{sanitized_query}%'

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM sightings
                WHERE location LIKE ? ESCAPE '\\'
                   OR notes LIKE ? ESCAPE '\\'
                ORDER BY timestamp DESC
            ''', (search_pattern, search_pattern))
            return [dict(row) for row in cursor.fetchall()]

    # ===================================================================
    # User Management Methods
    # ===================================================================

    def create_user(self, username: str, email: str, password: str,
                    role: str = 'resident', full_name: Optional[str] = None) -> int:
        """
        Create a new user account.

        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)
            role: User role (admin, resident, property_manager)
            full_name: Optional full name

        Returns:
            int: ID of newly created user

        Raises:
            ValueError: If validation fails or user already exists
        """
        # Validate inputs
        if not username or not isinstance(username, str) or len(username.strip()) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not email or not isinstance(email, str) or '@' not in email:
            raise ValueError("Valid email address is required")
        if not password or not isinstance(password, str) or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if role not in ('admin', 'resident', 'property_manager'):
            raise ValueError("Invalid role. Must be admin, resident, or property_manager")

        username = username.strip().lower()
        email = email.strip().lower()
        password_hash = generate_password_hash(password)

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, role, full_name)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, email, password_hash, role, full_name))
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            if 'username' in str(e).lower():
                raise ValueError("Username already exists")
            elif 'email' in str(e).lower():
                raise ValueError("Email already exists")
            else:
                raise ValueError("User creation failed")

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Retrieve a user by ID.

        Args:
            user_id: User ID

        Returns:
            Dict or None: User data

        Raises:
            ValueError: If user_id is invalid
        """
        if not isinstance(user_id, int) or user_id < 1:
            raise ValueError("User ID must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Retrieve a user by username.

        Args:
            username: Username to search for

        Returns:
            Dict or None: User data

        Raises:
            ValueError: If username is invalid
        """
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string")

        username = username.strip().lower()

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Retrieve a user by email.

        Args:
            email: Email to search for

        Returns:
            Dict or None: User data

        Raises:
            ValueError: If email is invalid
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")

        email = email.strip().lower()

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def verify_user_password(self, username: str, password: str) -> Optional[Dict]:
        """
        Verify user credentials and return user data if valid.

        Args:
            username: Username
            password: Plain text password

        Returns:
            Dict or None: User data if credentials valid, None otherwise

        Raises:
            ValueError: If inputs are invalid
        """
        if not username or not password:
            raise ValueError("Username and password are required")

        user = self.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            # Update last login
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET last_login = ? WHERE id = ?',
                    (datetime.now().isoformat(), user['id'])
                )
            return user
        return None

    def update_user(self, user_id: int, data: Dict) -> bool:
        """
        Update user information.

        Args:
            user_id: User ID
            data: Dictionary with fields to update

        Returns:
            bool: True if successful

        Raises:
            ValueError: If validation fails
        """
        if not isinstance(user_id, int) or user_id < 1:
            raise ValueError("User ID must be a positive integer")
        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary")

        # Build update query dynamically based on provided fields
        allowed_fields = {'email', 'full_name', 'role', 'is_active', 'password_hash'}
        update_fields = []
        values = []

        for field, value in data.items():
            if field in allowed_fields:
                update_fields.append(f'{field} = ?')
                values.append(value)

        if not update_fields:
            raise ValueError("No valid fields to update")

        # Add updated_at timestamp
        update_fields.append('updated_at = ?')
        values.append(datetime.now().isoformat())
        values.append(user_id)

        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            raise ValueError("Update failed: Email may already exist")

    def update_user_password(self, user_id: int, new_password: str) -> bool:
        """
        Update user password.

        Args:
            user_id: User ID
            new_password: New plain text password

        Returns:
            bool: True if successful

        Raises:
            ValueError: If validation fails
        """
        if not isinstance(user_id, int) or user_id < 1:
            raise ValueError("User ID must be a positive integer")
        if not new_password or len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters")

        password_hash = generate_password_hash(new_password)
        return self.update_user(user_id, {'password_hash': password_hash})

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user account.

        Args:
            user_id: User ID

        Returns:
            bool: True if successful

        Raises:
            ValueError: If user_id is invalid
        """
        if not isinstance(user_id, int) or user_id < 1:
            raise ValueError("User ID must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            return cursor.rowcount > 0

    def get_all_users(self, role: Optional[str] = None) -> List[Dict]:
        """
        Get all users, optionally filtered by role.

        Args:
            role: Optional role filter

        Returns:
            List[Dict]: List of user records
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if role:
                cursor.execute('SELECT * FROM users WHERE role = ? ORDER BY created_at DESC', (role,))
            else:
                cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]

    # ===================================================================
    # Property Management Methods
    # ===================================================================

    def create_property(self, name: str, created_by: int, address: Optional[str] = None) -> int:
        """
        Create a new property.

        Args:
            name: Property name
            created_by: User ID of creator
            address: Optional address

        Returns:
            int: ID of newly created property

        Raises:
            ValueError: If validation fails
        """
        if not name or not isinstance(name, str) or len(name.strip()) < 1:
            raise ValueError("Property name is required")
        if not isinstance(created_by, int) or created_by < 1:
            raise ValueError("Valid creator user ID is required")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO properties (name, address, created_by)
                VALUES (?, ?, ?)
            ''', (name.strip(), address, created_by))
            return cursor.lastrowid

    def get_property(self, property_id: int) -> Optional[Dict]:
        """
        Retrieve a property by ID.

        Args:
            property_id: Property ID

        Returns:
            Dict or None: Property data

        Raises:
            ValueError: If property_id is invalid
        """
        if not isinstance(property_id, int) or property_id < 1:
            raise ValueError("Property ID must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_properties(self) -> List[Dict]:
        """
        Get all properties.

        Returns:
            List[Dict]: List of property records
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM properties ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]

    def assign_user_to_property(self, user_id: int, property_id: int,
                                relationship_type: str = 'resident') -> bool:
        """
        Assign a user to a property.

        Args:
            user_id: User ID
            property_id: Property ID
            relationship_type: Type of relationship (owner, manager, resident)

        Returns:
            bool: True if successful

        Raises:
            ValueError: If validation fails
        """
        if not isinstance(user_id, int) or user_id < 1:
            raise ValueError("User ID must be a positive integer")
        if not isinstance(property_id, int) or property_id < 1:
            raise ValueError("Property ID must be a positive integer")
        if relationship_type not in ('owner', 'manager', 'resident'):
            raise ValueError("Invalid relationship type")

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_properties (user_id, property_id, relationship_type)
                    VALUES (?, ?, ?)
                ''', (user_id, property_id, relationship_type))
                return True
        except sqlite3.IntegrityError:
            # Already assigned, update relationship type
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE user_properties
                    SET relationship_type = ?
                    WHERE user_id = ? AND property_id = ?
                ''', (relationship_type, user_id, property_id))
                return cursor.rowcount > 0

    def get_user_properties(self, user_id: int) -> List[Dict]:
        """
        Get all properties associated with a user.

        Args:
            user_id: User ID

        Returns:
            List[Dict]: List of properties with relationship info

        Raises:
            ValueError: If user_id is invalid
        """
        if not isinstance(user_id, int) or user_id < 1:
            raise ValueError("User ID must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, up.relationship_type
                FROM properties p
                JOIN user_properties up ON p.id = up.property_id
                WHERE up.user_id = ?
                ORDER BY p.created_at DESC
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_property_users(self, property_id: int) -> List[Dict]:
        """
        Get all users associated with a property.

        Args:
            property_id: Property ID

        Returns:
            List[Dict]: List of users with relationship info

        Raises:
            ValueError: If property_id is invalid
        """
        if not isinstance(property_id, int) or property_id < 1:
            raise ValueError("Property ID must be a positive integer")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.*, up.relationship_type
                FROM users u
                JOIN user_properties up ON u.id = up.user_id
                WHERE up.property_id = ?
                ORDER BY up.created_at DESC
            ''', (property_id,))
            return [dict(row) for row in cursor.fetchall()]


# ===================================================================
# Flask-Login User Class
# ===================================================================

class User:
    """
    User class for Flask-Login integration.
    Wraps user data from the database.
    """

    def __init__(self, user_data: Dict):
        """
        Initialize User object from database row.

        Args:
            user_data: Dictionary containing user data from database
        """
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.role = user_data['role']
        self.full_name = user_data.get('full_name')
        self.is_active = bool(user_data.get('is_active', 1))
        self.last_login = user_data.get('last_login')
        self.created_at = user_data.get('created_at')

    def get_id(self):
        """Return user ID as string (required by Flask-Login)."""
        return str(self.id)

    @property
    def is_authenticated(self):
        """Return True if user is authenticated (required by Flask-Login)."""
        return True

    @property
    def is_anonymous(self):
        """Return False as this is not an anonymous user (required by Flask-Login)."""
        return False

    def is_admin(self):
        """Check if user has admin role."""
        return self.role == 'admin'

    def is_property_manager(self):
        """Check if user has property manager role."""
        return self.role == 'property_manager'

    def is_resident(self):
        """Check if user has resident role."""
        return self.role == 'resident'

    def __repr__(self):
        """String representation of User object."""
        return f'<User {self.username} ({self.role})>'
