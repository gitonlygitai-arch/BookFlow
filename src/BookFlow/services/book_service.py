from repositories import book_repository, author_repository, reservation_repository

def create_book(name: str, isbn: str, author_id: int):
    if not name.strip():
        raise Exception("Название книги не может быть пустым")
    if not isbn.strip():
        raise Exception("ISBN не может быть пустым")
    
    if not author_repository.get_by_id(author_id):
        raise Exception("Указанный автор не найден")

    book_id = book_repository.create(name.strip(), isbn.strip())
    book_repository.link_author(book_id, author_id)
    return book_id

def get_books():
    return book_repository.get_all()

def is_book_available(book_id: int) -> bool:
    return not reservation_repository.is_book_reserved(book_id) if hasattr(reservation_repository, 'is_book_reserved') else True