from dataclasses import dataclass

@dataclass
class Reservation:
    reservation_id: int
    librarian_id: int | None
    reader_id: int
    book_id: int
    reserved_at: str
    status: int  # 1 - Активна, 2 - Возвращена, 3 - Отменена
    status_name: str | None = None
    book_name: str | None = None
    reader_full_name: str | None = None