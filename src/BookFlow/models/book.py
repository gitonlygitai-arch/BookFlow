from dataclasses import dataclass

@dataclass
class Book:
    book_id: int
    name: str
    isbn: str