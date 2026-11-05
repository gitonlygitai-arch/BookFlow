from database.database import get_connection

def init_db():
    """Создает все таблицы в базе данных, если их еще нет."""
    conn = get_connection()
    cur = conn.cursor()

    # 1. Таблица пользователей (для авторизации и ролей)
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

    # 2. Таблица авторов (нужна для связи с книгами)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            patronymic TEXT
        )
    """)

    # 3. Таблица книг (используем name и isbn, как в твоем репозитории)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            isbn TEXT
        )
    """)

    # 4. Таблица связи книг и авторов (многие-ко-многим)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS author_books (
            book_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            PRIMARY KEY (book_id, author_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
            FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
        )
    """)

    # 5. Таблица выдач/бронирований (для бизнес-логики)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            loan_date TEXT DEFAULT CURRENT_TIMESTAMP,
            return_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ База данных успешно инициализирована. Все таблицы созданы.")