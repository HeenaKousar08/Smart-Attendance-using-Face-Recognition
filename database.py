import sqlite3
import hashlib
import pandas as pd
from datetime import datetime

DB_NAME = "attendance.db"

def init_db():
    """Initializes the SQLite database with the correct columns."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Attendance Logs Table (Including userid)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        userid TEXT, 
        time TEXT,
        date TEXT
    )""")
    
    # 2. Admin Users Table (For login functionality)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT UNIQUE, 
        password TEXT
    )""")
    
    conn.commit()
    conn.close()

def login_user(username, password):
    """Verifies admin credentials."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    data = cursor.fetchone()
    conn.close()
    return True if data else False

def insert_attendance(name, userid, time, date):
    """
    Records attendance. 
    Prevents duplicate entries for the same User ID on the same day.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if this specific ID is already marked for today
    cursor.execute("SELECT * FROM logs WHERE userid=? AND date=?", (userid, date))
    
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO logs (name, userid, time, date) VALUES (?, ?, ?, ?)", 
                       (name, userid, time, date))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

def get_all_records():
    """Fetches all records for the 'Records' tab in the UI."""
    conn = sqlite3.connect(DB_NAME)
    # Ensure userid is included in the dataframe
    df = pd.read_sql_query("SELECT name, userid, time, date FROM logs", conn)
    conn.close()
    return df