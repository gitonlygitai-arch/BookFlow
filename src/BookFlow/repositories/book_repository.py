from database.database import get_connection
from models.book import Book

def _get_name_column(cur) -> str:
    """Автоматически определяет, как называется колонка с наименованием книги в базе данных."""
    cur.execute("PRAGMA table_info(books)")
    columns = [row[1] for row in cur.fetchall()]
    for col in ['title', 'name', 'book_name', 'book_title']:
        if col in columns:
            return col
    # Если ничего из списка не нашлось, берем вторую колонку (после ID)
    return columns[1] if len(columns) > 1 else 'name'

def create(name: str, isbn: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    name_col = _get_name_column(cur)
    
    cur.execute(f"INSERT INTO books ({name_col}, isbn) VALUES (?, ?)", (name, isbn))
    conn.commit()
    bid = cur.lastrowid
    conn.close()
    return bid

def get_all() -> list[Book]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    conn.close()
    
    books = []
    for row in rows:
        row_dict = dict(zip(col_names, row))
        # Находим ID, название и ISBN независимо от имен колонок
        b_id = row_dict.get('book_id') or row_dict.get('id') or row[0]
        isbn = row_dict.get('isbn', '')
        
        # Ищем колонку с названием
        b_name = None
        for key in ['title', 'name', 'book_name', 'book_title']:
            if key in row_dict:
                b_name = row_dict[key]
                break
        if b_name is None and len(row) > 1:
            b_name = str(row[1])
            
        books.append(Book(book_id=b_id, name=b_name, isbn=isbn))
    return books

def get_by_id(book_id: int) -> Book | None:
    conn = get_connection()
    cur = conn.cursor()
    # Пробуем найти по первичному ключу book_id или id
    try:
        cur.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    except sqlite3.OperationalError:
        cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
        
    col_names = [description[0] for description in cur.description]
    conn.close()
    
    row_dict = dict(zip(col_names, row))
    b_id = row_dict.get('book_id') or row_dict.get('id', book_id)
    isbn = row_dict.get('isbn', '')
    
    b_name = None
    for key in ['title', 'name', 'book_name', 'book_title']:
        if key in row_dict:
            b_name = row_dict[key]
            break
    if b_name is None and len(row) > 1:
        b_name = str(row[1])
        
    return Book(book_id=b_id, name=b_name, isbn=isbn)

def link_author(book_id: int, author_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO author_books (book_id, author_id) VALUES (?, ?)", (book_id, author_id))
    conn.commit()
    conn.close()