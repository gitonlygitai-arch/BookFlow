from dataclasses import dataclass

@dataclass
class Author:
    author_id: int
    name: str
    surname: str
    patronymic: str | None = None