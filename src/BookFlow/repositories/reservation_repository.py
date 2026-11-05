from database.database import get_connection
from models.reservation import Reservation

def create(reader_id: int, book_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reservations (librarian_id, reader_id, book_id, reserved_at, status)
        VALUES (NULL, ?, ?, datetime('now'), 1)
    """, (reader_id, book_id))
    conn.commit()
    conn.close()

def get_by_id(reservation_id: int) -> Reservation | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.reservation_id, r.librarian_id, r.reader_id, r.book_id, r.reserved_at, r.status,
               b.name, u.surname || ' ' || u.name
        FROM reservations r
        JOIN books b ON r.book_id = b.book_id
        JOIN users u ON r.reader_id = u.user_id
        WHERE r.reservation_id = ?
    """, (reservation_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    status_map = {1: "Активна", 2: "Возвращена", 3: "Отменена"}
    return Reservation(row[0], row[1], row[2], row[3], row[4], row[5], status_map.get(row[5], "Неизвестно"), row[6], row[7])

def get_all() -> list[Reservation]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.reservation_id, r.librarian_id, r.reader_id, r.book_id, r.reserved_at, r.status,
               b.name, u.surname || ' ' || u.name
        FROM reservations r
        JOIN books b ON r.book_id = b.book_id
        JOIN users u ON r.reader_id = u.user_id
        ORDER BY r.reserved_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    status_map = {1: "Активна", 2: "Возвращена", 3: "Отменена"}
    result = []
    for r in rows:
        result.append(Reservation(r[0], r[1], r[2], r[3], r[4], r[5], status_map.get(r[5], "Неизвестно"), r[6], r[7]))
    return result

def update_status(reservation_id: int, status: int, librarian_id: int | None = None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE reservations
        SET status = ?, librarian_id = COALESCE(?, librarian_id)
        WHERE reservation_id = ?
    """, (status, librarian_id, reservation_id))
    conn.commit()
    conn.close()