import sqlite3
import os
from datetime import datetime

DB_NAME = "bizcalc.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite database with all tables."""
    if os.path.exists(DB_NAME):
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            industry TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        );
        
        CREATE TABLE revenue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            source TEXT,
            date DATE NOT NULL,
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        );
        
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            description TEXT,
            date DATE NOT NULL,
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        );
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

# --- CRUD Operations ---

def add_business(name, industry=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO businesses (name, industry) VALUES (?, ?)", (name, industry))
    conn.commit()
    business_id = cursor.lastrowid
    conn.close()
    return business_id

def get_businesses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM businesses ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_business(business_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM investments WHERE business_id = ?", (business_id,))
    cursor.execute("DELETE FROM revenue WHERE business_id = ?", (business_id,))
    cursor.execute("DELETE FROM expenses WHERE business_id = ?", (business_id,))
    cursor.execute("DELETE FROM businesses WHERE id = ?", (business_id,))
    conn.commit()
    conn.close()

def add_investment(business_id, amount, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO investments (business_id, amount, description, date) VALUES (?, ?, ?, ?)",
        (business_id, amount, description, date)
    )
    conn.commit()
    conn.close()

def add_revenue(business_id, amount, source, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO revenue (business_id, amount, source, date) VALUES (?, ?, ?, ?)",
        (business_id, amount, source, date)
    )
    conn.commit()
    conn.close()

def add_expense(business_id, amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (business_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
        (business_id, amount, category, description, date)
    )
    conn.commit()
    conn.close()

def get_transactions(business_id, table):
    """Get all transactions for a business from specified table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE business_id = ? ORDER BY date DESC", (business_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_totals(business_id):
    """Get total investment, revenue, and expenses for a business."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM investments WHERE business_id = ?", (business_id,))
    total_investment = cursor.fetchone()[0]
    
    cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM revenue WHERE business_id = ?", (business_id,))
    total_revenue = cursor.fetchone()[0]
    
    cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE business_id = ?", (business_id,))
    total_expenses = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_investment": float(total_investment),
        "total_revenue": float(total_revenue),
        "total_expenses": float(total_expenses)
    }