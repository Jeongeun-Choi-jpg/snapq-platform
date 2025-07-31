import sqlite3

# 데이터베이스 연결 (없으면 자동 생성)
conn = sqlite3.connect("my_words.db")
cur = conn.cursor()

# 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS my_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    word TEXT,
    meaning TEXT,
    correct_count INTEGER DEFAULT 0,
    review_date TEXT DEFAULT CURRENT_DATE
)
""")

conn.commit()
conn.close()

print("✅ my_words.db가 성공적으로 생성되었습니다.")
