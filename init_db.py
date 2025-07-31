import sqlite3

conn = sqlite3.connect('snapq.db')
c = conn.cursor()

# 학생별 범주별 레벨 기록 테이블
c.execute('''
CREATE TABLE IF NOT EXISTS users_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    category TEXT NOT NULL,
    level INTEGER DEFAULT 1
)
''')

conn.commit()
conn.close()
print("✅ users_progress 테이블 생성 완료")
