import os
import sqlite3
import hashlib
import uuid
from datetime import datetime

DB_PATH = "data/safety.db"

def get_db_connection():
    """Establishes and returns a connection to SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password, salt=None):
    """Securely hashes a password using SHA-256 and a unique salt."""
    if salt is None:
        salt = uuid.uuid4().hex
    
    # Hash password combined with salt
    hash_obj = hashlib.sha256((salt + password).encode())
    hashed_password = hash_obj.hexdigest()
    return hashed_password, salt

def init_db():
    """Initializes database tables and creates default user accounts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Check if we need to migrate reports table from old schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reports'")
    if cursor.fetchone():
        cursor.execute("PRAGMA table_info(reports)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'hobli' not in columns:
            print("Detected old database schema. Recreating reports table for villages...")
            cursor.execute("DROP TABLE reports")
            
    # Create Reports table (Crowdsourced and police incidents)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            state TEXT NOT NULL,
            district TEXT NOT NULL,
            taluk TEXT NOT NULL,
            hobli TEXT NOT NULL,
            village TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            incident_type TEXT NOT NULL,
            description TEXT,
            severity TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    
    conn.commit()
    
    # Preseed accounts if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        print("Pre-seeding default database users...")
        default_users = [
            ("admin", "admin123", "admin@womensafety.in", "Administrator"),
            ("police", "police123", "officer@police.gov.in", "Law Enforcement"),
            ("citizen", "citizen123", "citizen@gmail.com", "Citizen"),
            ("varsha", "varsha123", "varsha@gmail.com", "Citizen")
        ]
        for uname, pwd, email, role in default_users:
            hashed_pwd, salt = hash_password(pwd)
            try:
                cursor.execute(
                    "INSERT INTO users (username, password_hash, salt, email, role) VALUES (?, ?, ?, ?, ?)",
                    (uname, hashed_pwd, salt, email, role)
                )
            except sqlite3.IntegrityError:
                pass
        conn.commit()
        
    conn.close()
    print("SQLite database initialized successfully.")

def add_user(username, password, email, role="Citizen"):
    """Registers a new user in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pwd, salt = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, salt, email, role) VALUES (?, ?, ?, ?, ?)",
            (username, hashed_pwd, salt, email, role)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success

def verify_user(username, password):
    """Verifies user credentials. Returns user details if valid, else None."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        stored_hash = user['password_hash']
        stored_salt = user['salt']
        test_hash, _ = hash_password(password, stored_salt)
        if test_hash == stored_hash:
            return {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role']
            }
    return None

def add_report(username, state, district, taluk, hobli, village, latitude, longitude, incident_type, description, severity):
    """Saves a user safety/crime report to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO reports (username, state, district, taluk, hobli, village, latitude, longitude, incident_type, description, severity, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
        """, (username, state, district, taluk, hobli, village, latitude, longitude, incident_type, description, severity))
        conn.commit()
        success = True
    except Exception as e:
        print(f"Error saving report: {e}")
        success = False
    finally:
        conn.close()
    return success

def get_reports(state=None, district=None, taluk=None, hobli=None, village=None, include_resolved=False):
    """Retrieves reports from database, optionally filtered by state, district, taluk, hobli, or village."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM reports"
    params = []
    
    conditions = []
    if state:
        conditions.append("state = ?")
        params.append(state)
    if district:
        conditions.append("district = ?")
        params.append(district)
    if taluk:
        conditions.append("taluk = ?")
        params.append(taluk)
    if hobli:
        conditions.append("hobli = ?")
        params.append(hobli)
    if village:
        conditions.append("village = ?")
        params.append(village)
        
    if not include_resolved:
        conditions.append("status != 'Resolved'")
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY reported_at DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    # Convert list of rows to list of dicts
    reports = [dict(row) for row in rows]
    return reports

def update_report_status(report_id, new_status):
    """Updates the status of an incident report (e.g. 'Pending' -> 'Investigating' -> 'Resolved')."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE reports SET status = ? WHERE id = ?", (new_status, report_id))
        conn.commit()
        success = True
    except Exception as e:
        print(f"Error updating report status: {e}")
        success = False
    finally:
        conn.close()
    return success

if __name__ == "__main__":
    init_db()
