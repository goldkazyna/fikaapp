import sqlite3
from datetime import datetime

DB_PATH = "database/fika.db"


def init_db():
    """Создание таблиц"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Таблица платежей
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT UNIQUE,
            table_num TEXT,
            order_id TEXT,
            amount INTEGER,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def create_payment(payment_id: str, table_num: str, order_id: str, amount: int):
    """Создать запись о платеже"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Удаляем старый pending платёж для этого стола если есть
    c.execute('''
        DELETE FROM payments 
        WHERE table_num = ? AND status = 'pending'
    ''', (table_num,))
    
    c.execute('''
        INSERT INTO payments (payment_id, table_num, order_id, amount)
        VALUES (?, ?, ?, ?)
    ''', (payment_id, table_num, order_id, amount))
    
    conn.commit()
    conn.close()


def get_payment(payment_id: str):
    """Получить платёж по ID"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM payments WHERE payment_id = ?', (payment_id,))
    row = c.fetchone()
    
    conn.close()
    return dict(row) if row else None


def update_payment_status(payment_id: str, status: str):
    """Обновить статус платежа"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    paid_at = datetime.now() if status == 'paid' else None
    
    c.execute('''
        UPDATE payments 
        SET status = ?, paid_at = ?
        WHERE payment_id = ?
    ''', (status, paid_at, payment_id))
    
    conn.commit()
    conn.close()