from database.schema import init_db
from repositories.book_repository import create

init_db()
create("Война и мир", "978-5-04-116555-1")
create("Преступление и наказание", "978-5-04-116556-8")
print("Книги добавлены!")