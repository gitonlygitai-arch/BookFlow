import sqlite3
import os

def init_db():
    db_file = 'library.db'
    
    # Подключение к базе данных SQLite
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Выполнение SQL-скрипта из schema.sql
    if os.path.exists('schema.sql'):
        with open('schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        print("База данных SQLite успешно создана и заполнена тестовыми данными!")
    else:
        print("Файл schema.sql не найден!")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()