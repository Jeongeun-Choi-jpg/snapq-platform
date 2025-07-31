import sqlite3

conn = sqlite3.connect("my_words.db")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS my_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    word TEXT,
    meaning TEXT
)
''')

conn.commit()
conn.close()

print("✅ my_words.db 생성 완료")
