import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "bookflow.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Автоматически создает все необходимые таблицы, если они еще не существуют."""
    conn = get_connection()
    cur = conn.cursor()
    
    # Таблица пользователей
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        patronymic TEXT,
        password_hash TEXT NOT NULL,
        user_role INTEGER NOT NULL
    )
    """)
    
    # Таблица авторов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        patronymic TEXT
    )
    """)
    
    # Таблица книг (поддерживает и title, и name)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        isbn TEXT NOT NULL
    )
    """)
    
    # Связь книг и авторов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS author_books (
        book_id INTEGER,
        author_id INTEGER,
        FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE
    )
    """)
    
    # Таблица бронирований (теперь она точно будет создана!)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        librarian_id INTEGER,
        reader_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        reserved_at TEXT NOT NULL,
        status INTEGER NOT NULL,
        FOREIGN KEY(reader_id) REFERENCES users(user_id),
        FOREIGN KEY(librarian_id) REFERENCES users(user_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id)
    )
    """)
    
    conn.commit()
    conn.close()

# Инициализируем базу данных при импорте модуля
init_db()