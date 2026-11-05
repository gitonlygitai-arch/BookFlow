from database.database import get_connection

def seed_database():
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Очищаем таблицы в правильном порядке
    cur.execute("DELETE FROM reservations")
    cur.execute("DELETE FROM author_books")
    cur.execute("DELETE FROM books")
    cur.execute("DELETE FROM authors")
    
    # 2. Сбрасываем счетчики AUTOINCREMENT в SQLite
    cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('authors', 'books', 'reservations')")
    
    # 3. Список авторов (8 человек)
    authors = [
        ("Лев", "Толстой", "Николаевич"),           # ID 1
        ("Александр", "Пушкин", "Сергеевич"),       # ID 2
        ("Фёдор", "Достоевский", "Михайлович"),     # ID 3
        ("Антон", "Чехов", "Павлович"),             # ID 4
        ("Михаил", "Лермонтов", "Юрьевич"),         # ID 5
        ("Николай", "Гоголь", "Васильевич"),        # ID 6
        ("Иван", "Тургенев", "Сергеевич"),          # ID 7
        ("Сергей", "Есенин", "Александрович")       # ID 8
    ]
    
    cur.executemany("INSERT INTO authors (name, surname, patronymic) VALUES (?, ?, ?)", authors)
    
    # Определяем имя колонки для названия книги (title или name)
    cur.execute("PRAGMA table_info(books)")
    columns = [row[1] for row in cur.fetchall()]
    book_col = 'title' if 'title' in columns else ('name' if 'name' in columns else columns[1])

    # 4. Список книг (8 произведений)
    books = [
        ("Война и мир", "978-5-17-090123-4", 1),
        ("Евгений Онегин", "978-5-699-12345-6", 2),
        ("Преступление и наказание", "978-5-04-100234-5", 3),
        ("Вишневый сад", "978-5-699-76543-2", 4),
        ("Герой нашего времени", "978-5-17-112233-4", 5),
        ("Мертвые души", "978-5-04-998877-6", 6),
        ("Отцы и дети", "978-5-699-445566-7", 7),
        ("Черный человек", "978-5-17-334455-8", 8)
    ]
    
    for title, isbn, author_id in books:
        cur.execute(f"INSERT INTO books ({book_col}, isbn) VALUES (?, ?)", (title, isbn))
        book_id = cur.lastrowid
        cur.execute("INSERT INTO author_books (book_id, author_id) VALUES (?, ?)", (book_id, author_id))

    conn.commit()
    conn.close()
    print("✅ База данных успешно очищена и заполнена 8 авторами и 8 книгами!")

if __name__ == "__main__":
    seed_database()