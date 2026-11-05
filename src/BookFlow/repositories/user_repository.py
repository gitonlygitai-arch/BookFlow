from database.database import get_connection
from models.user import User

def _map(row) -> User:
    return User(*row)

def create(name: str, surname: str, patronymic: str | None, password_hash: str, user_role: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (name, surname, patronymic, password_hash, user_role)
        VALUES (?, ?, ?, ?, ?)
    """, (name, surname, patronymic, password_hash, user_role))
    conn.commit()
    uid = cur.lastrowid
    conn.close()
    return uid

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, surname, patronymic, password_hash, user_role FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, surname, patronymic, password_hash, user_role FROM users")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update_role(user_id: int, new_role: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET user_role = ? WHERE user_id = ?", (new_role, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()