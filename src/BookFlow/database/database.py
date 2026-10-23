import sqlite3
import os

def init_db():
    # Поднимаемся на уровень выше в корень проекта к файлу базы и схемы
    db_path = os.path.join(os.path.dirname(__file__), '../library.db')
    schema_path = os.path.join(os.path.dirname(__file__), '../schema.sql')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_script = f.read()
        cursor.executescript(schema_script)

    conn.commit()
    conn.close()
    print("База данных успешно инициализирована из структуры!")

if __name__ == '__main__':
    init_db()