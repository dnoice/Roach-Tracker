"""
File: models.py
Path: app/models.py
Purpose: Database schema and operations for roach sighting tracking
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from contextlib import contextmanager


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
        Creates the sightings table with all required fields.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sightings (
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
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def create_sighting(self, data: Dict) -> int:
        """
        Create a new roach sighting record.

        Args:
            data: Dictionary containing sighting information

        Returns:
            int: ID of newly created sighting
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sightings (
                    timestamp, location, room_type, roach_count,
                    roach_size, roach_type, photo_path, notes,
                    weather, temperature, time_of_day
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('timestamp', datetime.now().isoformat()),
                data['location'],
                data.get('room_type'),
                data.get('roach_count', 1),
                data.get('roach_size'),
                data.get('roach_type'),
                data.get('photo_path'),
                data.get('notes'),
                data.get('weather'),
                data.get('temperature'),
                data.get('time_of_day')
            ))
            return cursor.lastrowid

    def get_sighting(self, sighting_id: int) -> Optional[Dict]:
        """
        Retrieve a single sighting by ID.

        Args:
            sighting_id: ID of the sighting

        Returns:
            Dict or None: Sighting data as dictionary
        """
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
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM sightings ORDER BY timestamp DESC'
            if limit:
                query += f' LIMIT {limit} OFFSET {offset}'
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def update_sighting(self, sighting_id: int, data: Dict) -> bool:
        """
        Update an existing sighting record.

        Args:
            sighting_id: ID of the sighting to update
            data: Dictionary containing updated fields

        Returns:
            bool: True if update successful
        """
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
                    updated_at = ?
                WHERE id = ?
            ''', (
                data.get('timestamp'),
                data['location'],
                data.get('room_type'),
                data.get('roach_count', 1),
                data.get('roach_size'),
                data.get('roach_type'),
                data.get('photo_path'),
                data.get('notes'),
                data.get('weather'),
                data.get('temperature'),
                data.get('time_of_day'),
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
        """
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
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f'%{query}%'
            cursor.execute('''
                SELECT * FROM sightings
                WHERE location LIKE ? OR notes LIKE ?
                ORDER BY timestamp DESC
            ''', (search_pattern, search_pattern))
            return [dict(row) for row in cursor.fetchall()]
