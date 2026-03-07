import sqlite3
import json
import os

DATABASE = 'reports.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            verified INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def seed_db_from_json(path='data/sample_reports.json'):
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
    if count == 0:
        with open(path, 'r') as f:
            reports = json.load(f)
        for r in reports:
            conn.execute('''
                INSERT INTO reports (title, description, category, severity, location, status, created_at, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (r['title'], r['description'], r['category'], r['severity'],
                  r['location'], r['status'], r['created_at'], int(r['verified'])))
        conn.commit()
    conn.close()

def fetch_reports(search=None, category=None, severity=None, status=None):
    conn = get_db_connection()
    query = 'SELECT * FROM reports WHERE 1=1'
    params = []
    if search:
        query += ' AND (title LIKE ? OR description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    if category:
        query += ' AND category = ?'
        params.append(category)
    if severity:
        query += ' AND severity = ?'
        params.append(severity)
    if status:
        query += ' AND status = ?'
        params.append(status)
    query += ' ORDER BY created_at DESC'
    reports = conn.execute(query, params).fetchall()
    conn.close()
    return reports

def insert_report(data):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO reports (title, description, category, severity, location, status, created_at, verified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['title'], data['description'], data['category'], data['severity'],
          data['location'], data['status'], data['created_at'], int(data['verified'])))
    conn.commit()
    conn.close()

def update_report_status(report_id, new_status):
    conn = get_db_connection()
    conn.execute('UPDATE reports SET status = ? WHERE id = ?', (new_status, report_id))
    conn.commit()
    conn.close()

def get_reports_for_digest(search=None, category=None, severity=None, status=None):
    return fetch_reports(search=search, category=category, severity=severity, status=status)
