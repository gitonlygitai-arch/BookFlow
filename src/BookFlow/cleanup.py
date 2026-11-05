from database.database import get_connection

conn = get_connection()
cur = conn.cursor()
# Удаляем авторов с ID > 3 (весь мусор)
cur.execute("DELETE FROM authors WHERE author_id > 3")
conn.commit()
conn.close()
print("✅ Мусорные авторы успешно удалены!")