# database.py - Complete working version
import sqlite3
import hashlib
import os
import re
from datetime import datetime

DB_PATH = "neurascan.db"

# ========== DB INIT ==========
def init_db():
    """Create the database and users table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name  TEXT    NOT NULL,
            last_name   TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            role        TEXT    NOT NULL DEFAULT 'other',
            password    TEXT    NOT NULL,
            created_at  TEXT    NOT NULL
        )
    """)
    
    # Create analysis history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_filename TEXT,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            probabilities TEXT,
            analysis_time REAL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("[NeuraScan DB] Database initialized successfully.")

# ========== PASSWORD HASHING ==========
def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return hash_password(plain_password) == hashed_password

# ========== VALIDATION HELPERS ==========
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email.strip()))

def is_valid_password(password: str) -> bool:
    """Min 8 characters."""
    return len(password) >= 8

ALLOWED_ROLES = {"student", "researcher", "doctor", "engineer", "other"}

def is_valid_role(role: str) -> bool:
    return role.strip().lower() in ALLOWED_ROLES

# ========== SIGNUP ==========
def signup_user(first_name: str, last_name: str, email: str,
                password: str, role: str = "other") -> dict:
    """Register a new user."""
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip().lower()
    role = role.strip().lower()

    if not first_name or not last_name:
        return {"success": False, "message": "First and last name are required."}

    if not is_valid_email(email):
        return {"success": False, "message": "Please enter a valid email address."}

    if not is_valid_password(password):
        return {"success": False, "message": "Password must be at least 8 characters."}

    if not is_valid_role(role):
        role = "other"

    hashed_pw = hash_password(password)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, role, password, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, email, role, hashed_pw, created_at))

        conn.commit()
        conn.close()

        print(f"[NeuraScan DB] New user registered: {email}")
        return {"success": True, "message": "Account created successfully!"}

    except sqlite3.IntegrityError:
        return {"success": False, "message": "An account with this email already exists."}

    except Exception as e:
        return {"success": False, "message": f"Database error: {str(e)}"}

# ========== LOGIN ==========
def login_user(email: str, password: str) -> dict:
    """Verify user credentials."""
    email = email.strip().lower()

    if not email or not password:
        return {"success": False, "message": "Email and password are required."}

    hashed_pw = hash_password(password)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, first_name, last_name, email, role, created_at
            FROM users
            WHERE email = ? AND password = ?
        """, (email, hashed_pw))

        row = cursor.fetchone()
        conn.close()

        if row:
            user = {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "role": row[4],
                "created_at": row[5],
            }
            print(f"[NeuraScan DB] User logged in: {email}")
            return {"success": True, "user": user}
        else:
            return {"success": False, "message": "Invalid email or password."}

    except Exception as e:
        return {"success": False, "message": f"Database error: {str(e)}"}

# ========== USER FUNCTIONS ==========
def get_user_by_id(user_id: int) -> dict | None:
    """Get user by ID."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name, email, role, created_at FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_user_by_email(email: str) -> dict | None:
    """Fetch a user record by email. Returns dict or None."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, first_name, last_name, email, role, created_at
            FROM users WHERE email = ?
        """, (email.strip().lower(),))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "role": row[4],
                "created_at": row[5],
            }
        return None

    except Exception as e:
        print(f"[NeuraScan DB] Error: {e}")
        return None

def email_exists(email: str) -> bool:
    """Check if an email is already registered."""
    return get_user_by_email(email) is not None

def get_all_users() -> list:
    """Return all registered users (admin use only)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, first_name, last_name, email, role, created_at FROM users
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "first_name": r[1],
                "last_name": r[2],
                "email": r[3],
                "role": r[4],
                "created_at": r[5],
            }
            for r in rows
        ]

    except Exception as e:
        print(f"[NeuraScan DB] Error: {e}")
        return []

def delete_user(email: str) -> bool:
    """Delete a user by email. Returns True if deleted."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email = ?", (email.strip().lower(),))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
    except Exception as e:
        print(f"[NeuraScan DB] Error: {e}")
        return False

# ========== ANALYSIS HISTORY FUNCTIONS ==========
def save_analysis(user_id, prediction, confidence, probabilities, image_filename=None, analysis_time=None):
    """Save analysis to history"""
    import json
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        probabilities_json = json.dumps(probabilities) if probabilities else None
        
        cursor.execute('''
            INSERT INTO analysis_history (user_id, image_filename, prediction, confidence, probabilities, analysis_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, image_filename, prediction, confidence, probabilities_json, analysis_time, created_at))
        
        conn.commit()
        analysis_id = cursor.lastrowid
        conn.close()
        
        return {'success': True, 'analysis_id': analysis_id}
    except Exception as e:
        print(f"Error saving analysis: {e}")
        return {'success': False, 'message': str(e)}

def get_user_history(user_id, limit=100):
    """Get user's analysis history"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, image_filename, prediction, confidence, analysis_time, created_at
            FROM analysis_history 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {'success': True, 'history': history}
    except Exception as e:
        print(f"Error getting history: {e}")
        return {'success': False, 'message': str(e), 'history': []}

def delete_analysis(analysis_id, user_id):
    """Delete analysis from history"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM analysis_history WHERE id = ? AND user_id = ?', (analysis_id, user_id))
        conn.commit()
        conn.close()
        return {'success': True, 'message': 'Analysis deleted'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

# ========== AUTO INIT ON IMPORT ==========
init_db()