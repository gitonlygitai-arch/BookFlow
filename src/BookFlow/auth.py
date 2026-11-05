import hashlib
from repositories import user_repository

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name: str, surname: str, patronymic: str | None, password: str, user_role: int = 1) -> int:
    if not name.strip() or not surname.strip() or not password.strip():
        raise Exception("Заполните обязательные поля")
    pwd_hash = _hash_password(password)
    return user_repository.create(name.strip(), surname.strip(), patronymic.strip() if patronymic else None, pwd_hash, user_role)

def authenticate(user_id: int, password: str):
    user = user_repository.get_by_id(user_id)
    if not user:
        return None
    if user.password_hash == _hash_password(password):
        return user
    return None