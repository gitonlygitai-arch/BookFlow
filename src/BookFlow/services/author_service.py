from repositories import author_repository

def create_author(name: str, surname: str, patronymic: str | None = None):
    if not name.strip():
        raise Exception("Имя не может быть пустым")
    if not surname.strip():
        raise Exception("Фамилия не может быть пустой")
    
    authors = author_repository.get_all()
    for a in authors:
        if (a.name.lower() == name.lower() and 
            a.surname.lower() == surname.lower() and 
            (a.patronymic or "").lower() == (patronymic or "").lower()):
            raise Exception("Автор уже существует")
            
    return author_repository.create(name.strip(), surname.strip(), patronymic.strip() if patronymic else None)

def get_authors():
    return author_repository.get_all()