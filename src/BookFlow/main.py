from database.schema import init_db
from menu import start_app  # <--- Берем из menu.py, а не из ui.menus

if __name__ == "__main__":
    init_db()
    start_app()
# пароль от бибиотекаря(2): 123, пароль от пользователя(2): 1234, администратора(3) 12