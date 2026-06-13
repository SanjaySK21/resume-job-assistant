# database.py

import sqlite3
import json
from datetime import datetime

DB_PATH = "database.db"


# ─────────────────────────────────────────
# Setup — run once when app starts
# ─────────────────────────────────────────

def init_db():
    """
    Creates the analyses table if it does not exist.
    Called once at app startup.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            fit_score   REAL,
            matched     TEXT,
            missing     TEXT,
            tips        TEXT,
            questions   TEXT,
            timestamp   DATETIME
        )
    """)

    conn.commit()
    conn.close()


# ─────────────────────────────────────────
# Save one analysis result
# ─────────────────────────────────────────

def save_analysis(resume_name, fit_score, matched, missing, tips, questions):
    """
    Saves one analysis to the database.
    Lists are stored as JSON strings — easy to read back later.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyses
        (resume_name, fit_score, matched, missing, tips, questions, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        resume_name,
        fit_score,
        json.dumps(matched),
        json.dumps(missing),
        tips,
        json.dumps(questions),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ─────────────────────────────────────────
# Read all past analyses
# ─────────────────────────────────────────

def get_all_analyses():
    """
    Returns all saved analyses from DB.
    Lists are parsed back from JSON strings.
    Returns list of dicts — easy to use in Streamlit.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, resume_name, fit_score, matched, missing,
               tips, questions, timestamp
        FROM analyses
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id":          row[0],
            "resume_name": row[1],
            "fit_score":   row[2],
            "matched":     json.loads(row[3]),
            "missing":     json.loads(row[4]),
            "tips":        row[5],
            "questions":   json.loads(row[6]),
            "timestamp":   row[7]
        })

    return results