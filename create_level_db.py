# create_level_db.py

import sqlite3

conn = sqlite3.connect("level_data.db")
cur = conn.cursor()

# 테이블이 없다면 생성
cur.execute('''
CREATE TABLE IF NOT EXISTS level (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    theme TEXT,
    level INTEGER
)
''')

conn.commit()
conn.close()
print("✅ level 테이블이 생성되었습니다.")
