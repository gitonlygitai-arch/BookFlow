-- Удаление старых таблиц
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS members;

-- 1. Таблица авторов
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- 2. Таблица книг (связана с авторами)
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER,
    year INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- 3. Таблица участников
CREATE TABLE members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL
);

-- 4. Таблица аренды (связывает участников и книги)
CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    book_id INTEGER,
    rental_period TEXT,
    returned INTEGER DEFAULT 0,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Добавление тестовых записей 
INSERT INTO authors (name) VALUES 
    ('Л.Н. Толстой'),
    ('Ф.М. Достоевский');

INSERT INTO books (title, author_id, year) VALUES 
    ('Война и мир', 1, 1869),
    ('Преступление и наказание', 2, 1866);

INSERT INTO members (full_name) VALUES 
    ('Серова В.П.');

INSERT INTO loans (member_id, book_id, rental_period, returned) VALUES 
    (1, 2, '13.10.2025-15.10.2025', 0);
