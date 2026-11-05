from repositories import reservation_repository, book_repository, user_repository

READER_ROLE_ID = 1

def create_reservation(reader_id: int, book_id: int):
    user = user_repository.get_by_id(reader_id)
    if not user or user.user_role != READER_ROLE_ID:
        raise Exception("Только читатель может бронировать")
        
    if not book_repository.get_by_id(book_id):
        raise Exception("Книга не найдена")
        
    # Проверка на доступность (нет активных броней со статусом 1)
    all_res = reservation_repository.get_all()
    for r in all_res:
        if r.book_id == book_id and r.status == 1:
            raise Exception("Книга занята")
            
    reservation_repository.create(reader_id, book_id)

def get_reservations():
    return reservation_repository.get_all()

def mark_returned(reservation_id: int, librarian_id: int):
    reservation_repository.update_status(reservation_id, status=2, librarian_id=librarian_id)

def cancel_reservation(reservation_id: int):
    reservation_repository.update_status(reservation_id, status=3)