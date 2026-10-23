import sqlite3
import os

def get_db_path():
    """Возвращает абсолютный путь к файлу базы данных в корне проекта."""
    # Поднимаемся из src/database/ на два уровня вверх до корня проекта
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../library.db'))

def get_schema_path():
    """Возвращает абсолютный путь к файлу схемы в корне проекта."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../schema.sql'))

def get_connection():
    """Создает и возвращает соединение с базой данных SQLite."""
    conn = sqlite3.connect(get_db_path())
    # Включаем поддержку внешних ключей (важно для SQLite)
    conn.execute("PRAGMA foreign_keys = ON;")
    # Устанавливаем row_factory, чтобы можно было обращаться к колонкам по именам словаря
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализирует базу данных, выполняя SQL-скрипт схемы."""
    schema_path = get_schema_path()
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Файл схемы не найден по пути: {schema_path}")

    conn = get_connection()
    cursor = conn.cursor()
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()
    print("База данных успешно инициализирована.")

if __name__ == "__main__":
    # Позволяет запустить файл напрямую для проверки создания БД
    init_db()