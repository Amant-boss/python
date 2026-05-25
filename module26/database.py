import sqlite3
from typing import List, Dict, Any, Optional

def create_connection():
    connection = sqlite3.connect("receipts.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        store TEXT NOT NULL,
        category TEXT NOT NULL,
        subtotal REAL NOT NULL,
        tax REAL NOT NULL,
        total_amount REAL NOT NULL,
        date TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

create_table()

def create_receipt(receipt_data: Dict[str, Any]) -> int:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO receipts (owner, store, category, subtotal, tax, total_amount, date) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        receipt_data["owner"],
        receipt_data["store"],
        receipt_data["category"],
        receipt_data["subtotal"],
        receipt_data["tax"],
        receipt_data["total_amount"],
        receipt_data["date"]
    ))
    connection.commit()
    receipt_id = cursor.lastrowid
    connection.close()
    return receipt_id

def read_receipts() -> List[Dict[str, Any]]:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM receipts")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def read_receipt(receipt_id: int) -> Optional[Dict[str, Any]]:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM receipts WHERE id = ?", (receipt_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return dict(row)

def update_receipt(receipt_id: int, receipt_data: Dict[str, Any]) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE receipts 
    SET owner = ?, store = ?, category = ?, subtotal = ?, tax = ?, total_amount = ?, date = ? 
    WHERE id = ?
    """, (
        receipt_data["owner"],
        receipt_data["store"],
        receipt_data["category"],
        receipt_data["subtotal"],
        receipt_data["tax"],
        receipt_data["total_amount"],
        receipt_data["date"],
        receipt_id
    ))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0

def delete_receipt(receipt_id: int) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM receipts WHERE id = ?", (receipt_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0
