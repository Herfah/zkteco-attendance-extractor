"""Database module for storing attendance records"""
import sqlite3
import os
from datetime import datetime
from config import config

class AttendanceDB:
    """SQLite database for attendance records"""
    
    def __init__(self):
        self.db_path = config.DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                user_name TEXT,
                timestamp DATETIME NOT NULL,
                status INTEGER,
                device_ip TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, timestamp, status)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                records_synced INTEGER,
                sync_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_attendance(self, user_id, user_name, timestamp, status, device_ip):
        """Insert attendance record"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO attendance (user_id, user_name, timestamp, status, device_ip)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_name, timestamp, status, device_ip))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error inserting record: {e}")
            return False
    
    def get_all_records(self):
        """Get all attendance records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM attendance ORDER BY timestamp DESC')
        records = cursor.fetchall()
        conn.close()
        return records
    
    def get_records_by_date(self, start_date, end_date):
        """Get records between dates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM attendance 
            WHERE DATE(timestamp) BETWEEN ? AND ?
            ORDER BY timestamp DESC
        ''', (start_date, end_date))
        records = cursor.fetchall()
        conn.close()
        return records
    
    def get_records_by_user(self, user_id):
        """Get records for specific user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM attendance 
            WHERE user_id = ?
            ORDER BY timestamp DESC
        ''', (user_id,))
        records = cursor.fetchall()
        conn.close()
        return records
    
    def log_sync(self, device_ip, records_synced, status, error_message=None):
        """Log sync operation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sync_log (device_ip, records_synced, status, error_message)
            VALUES (?, ?, ?, ?)
        ''', (device_ip, records_synced, status, error_message))
        conn.commit()
        conn.close()
    
    def delete_old_records(self, days=365):
        """Delete records older than specified days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM attendance 
            WHERE created_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted
