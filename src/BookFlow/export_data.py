import os
import sqlite3
import json
import csv
import xml.etree.ElementTree as ET
import yaml

# Путь к базе данных BookFlow
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "database", "bookflow.db")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "out")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def fetch_structured_data():
    """Извлекаем книги и связанных авторов с помощью JOIN"""
    conn = get_connection()
    cur = conn.cursor()

    # Узнаем реальное имя колонки названия книги ('title' или 'name')
    cur.execute("PRAGMA table_info(books)")
    columns = [row[1] for row in cur.fetchall()]
    book_col = "title" if "title" in columns else ("name" if "name" in columns else columns[1])

    query = f"""
        SELECT b.book_id, b.{book_col}, b.isbn,
               a.author_id, a.name, a.surname, a.patronymic
        FROM books b
        LEFT JOIN author_books ab ON b.book_id = ab.book_id
        LEFT JOIN authors a ON ab.author_id = a.author_id
    """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    books_dict = {}
    for row in rows:
        b_id, title, isbn, a_id, a_name, a_surname, a_patronymic = row

        if b_id not in books_dict:
            books_dict[b_id] = {
                "id": b_id,
                "title": title,
                "isbn": isbn,
                "authors": []
            }

        if a_id is not None:
            books_dict[b_id]["authors"].append({
                "author_id": a_id,
                "name": a_name,
                "surname": a_surname,
                "patronymic": a_patronymic or ""
            })

    return list(books_dict.values())

def main():
    # 1. Автоматически создаем папку out, если её нет
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    data = fetch_structured_data()
    if not data:
        print("⚠️ В базе нет данных. Сначала запустите seed.py!")
        return

    # 2. Экспорт в JSON
    with open(os.path.join(OUTPUT_DIR, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # 3. Экспорт в CSV
    with open(os.path.join(OUTPUT_DIR, "data.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "isbn", "authors"])
        for item in data:
            authors_str = "; ".join([f"{a['surname']} {a['name']}" for a in item["authors"]])
            writer.writerow([item["id"], item["title"], item["isbn"], authors_str])

    # 4. Экспорт в XML
    root = ET.Element("library")
    for item in data:
        book_elem = ET.SubElement(root, "book")
        ET.SubElement(book_elem, "id").text = str(item["id"])
        ET.SubElement(book_elem, "title").text = item["title"]
        ET.SubElement(book_elem, "isbn").text = item["isbn"]
        
        authors_elem = ET.SubElement(book_elem, "authors")
        for a in item["authors"]:
            author_elem = ET.SubElement(authors_elem, "author")
            ET.SubElement(author_elem, "author_id").text = str(a["author_id"])
            ET.SubElement(author_elem, "name").text = a["name"]
            ET.SubElement(author_elem, "surname").text = a["surname"]
            ET.SubElement(author_elem, "patronymic").text = a["patronymic"]
            
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ", level=0)
    tree.write(os.path.join(OUTPUT_DIR, "data.xml"), encoding="utf-8", xml_declaration=True)

    # 5. Экспорт в YAML
    with open(os.path.join(OUTPUT_DIR, "data.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        
    print(f"✅ Успешно! Все 4 файла сгенерированы в папке: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()