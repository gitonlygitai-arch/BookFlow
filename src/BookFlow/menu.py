from services import author_service, book_service, reservation_service
from repositories import user_repository
from auth import authenticate, register_user

def reader_menu(user):
    while True:
        print(f"\n===== Читатель ({user.surname} {user.name}) =====")
        print("1. Посмотреть каталог книг")
        print("2. Забронировать книгу")
        print("3. Посмотреть список авторов")
        print("0. Выход из аккаунта")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            books = book_service.get_books()
            print("\n-- Доступные книги --")
            for b in books:
                print(f"ID: {b.book_id} | Название: {b.name} | ISBN: {b.isbn}")
        elif choice == "2":
            try:
                book_id = int(input("Введите ID книги для бронирования: "))
                reservation_service.create_reservation(user.user_id, book_id)
                print("Книга успешно забронирована!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "3":
            authors = author_service.get_authors()
            print("\n-- Авторы --")
            for a in authors:
                print(f"ID: {a.author_id} | {a.surname} {a.name} {a.patronymic or ''}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")

def librarian_menu(user):
    while True:
        print(f"\n===== Библиотекарь ({user.surname} {user.name}) =====")
        print("1. Посмотреть каталог книг")
        print("2. Посмотреть список авторов")
        print("3. Добавить автора")
        print("4. Добавить книгу")
        print("5. Просмотреть бронирования / Управление")
        print("0. Выход из аккаунта")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            books = book_service.get_books()
            print("\n-- Каталог книг --")
            for b in books:
                print(f"ID: {b.book_id} | Название: {b.name} | ISBN: {b.isbn}")
        elif choice == "2":
            authors = author_service.get_authors()
            print("\n-- Список авторов --")
            for a in authors:
                print(f"ID: {a.author_id} | {a.surname} {a.name} {a.patronymic or ''}")
        elif choice == "3":
            try:
                name = input("Имя автора: ")
                surname = input("Фамилия автора: ")
                patronymic = input("Отчество (Enter если нет): ")
                author_service.create_author(name, surname, patronymic if patronymic else None)
                print("Автор успешно добавлен!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "4":
            try:
                name = input("Название книги: ")
                isbn = input("ISBN: ")
                author_id = int(input("ID автора книги: "))
                book_service.create_book(name, isbn, author_id)
                print("Книга успешно добавлена!")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "5":
            reservations = reservation_service.get_reservations()
            print("\n-- Все бронирования --")
            for r in reservations:
                print(f"Бронь #{r.reservation_id} | Книга: {r.book_name} | Читатель: {r.reader_full_name} | Статус: {r.status_name} | Дата: {r.reserved_at}")
            
            sub = input("\nИзменить статус брони? (1 - Отметить возвращенной, 2 - Отменить бронь, 0 - Назад): ")
            if sub == "1":
                try:
                    rid = int(input("Введите ID бронирования: "))
                    reservation_service.mark_returned(rid, user.user_id)
                    print("Статус обновлен: Возвращена.")
                except Exception as e:
                    print(f"Ошибка: {e}")
            elif sub == "2":
                try:
                    rid = int(input("Введите ID бронирования: "))
                    reservation_service.cancel_reservation(rid)
                    print("Бронирование отменено.")
                except Exception as e:
                    print(f"Ошибка: {e}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")

def admin_menu(user):
    while True:
        print(f"\n===== Администратор ({user.surname} {user.name}) =====")
        print("1. Посмотреть список всех пользователей")
        print("2. Изменить роль пользователя")
        print("3. Удалить пользователя")
        print("0. Выход из аккаунта")
        choice = input("Выберите действие: ")
        
        role_names = {1: "Читатель", 2: "Библиотекарь", 3: "Администратор"}

        if choice == "1":
            users = user_repository.get_all()
            print("\n-- Список пользователей системы --")
            for u in users:
                r_name = role_names.get(u.user_role, "Неизвестно")
                print(f"ID: {u.user_id} | {u.surname} {u.name} {u.patronymic or ''} | Роль: {r_name}")
        elif choice == "2":
            try:
                uid = int(input("Введите ID пользователя для смены роли: "))
                print("Доступные роли: 1 - Читатель, 2 - Библиотекарь, 3 - Администратор")
                new_role = int(input("Введите новую роль: "))
                if new_role in (1, 2, 3):
                    user_repository.update_role(uid, new_role)
                    print("Роль пользователя успешно обновлена!")
                else:
                    print("Неверная роль.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "3":
            try:
                uid = int(input("Введите ID пользователя для удаления: "))
                if uid == user.user_id:
                    print("Нельзя удалить собственный административный аккаунт!")
                    continue
                user_repository.delete_user(uid)
                print("Пользователь успешно удален.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")

def start_app():
    while True:
        print("\n=== ИС БИБЛИОТЕКА (BOOKFLOW) ===")
        print("1. Войти в систему")
        print("2. Зарегистрироваться")
        print("0. Выход")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            try:
                uid = int(input("Ваш ID пользователя: "))
                pwd = input("Пароль: ")
                user = authenticate(uid, pwd)
                if not user:
                    print("Неверный ID или пароль.")
                else:
                    if user.user_role == 3:
                        admin_menu(user)
                    elif user.user_role == 2:
                        librarian_menu(user)
                    else:
                        reader_menu(user)
            except ValueError:
                print("ID должен быть числом.")
        elif choice == "2":
            try:
                name = input("Имя: ")
                surname = input("Фамилия: ")
                patronymic = input("Отчество (Enter если нет): ")
                pwd = input("Пароль: ")
                print("Роли: 1 - Читатель, 2 - Библиотекарь, 3 - Администратор")
                role = int(input("Выберите роль: "))
                
                if role not in (1, 2, 3):
                    print("Ошибка: неверная роль.")
                    continue
                    
                uid = register_user(name, surname, patronymic if patronymic else None, pwd, user_role=role)
                role_names = {1: "Читатель", 2: "Библиотекарь", 3: "Администратор"}
                print(f"Регистрация ({role_names[role]}) успешна! Ваш выданный ID для входа: {uid}")
            except Exception as e:
                print(f"Ошибка регистрации: {e}")
        elif choice == "0":
            print("Выход из программы.")
            break