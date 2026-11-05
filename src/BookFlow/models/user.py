from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    name: str
    surname: str
    patronymic: str | None
    password_hash: str
    user_role: int  # 1 - Читатель, 2 - Библиотекарь