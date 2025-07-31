# pages/remind_wrong_words.py

import streamlit as st
from datetime import datetime, timedelta
import random
import os

st.set_page_config(page_title="📆 오답 복습 리마인더", layout="centered")
st.title("📆 날짜 기반 오답 복습")
st.markdown("#### 이름과 날짜 범위를 선택해 복습을 시작하세요!")

# ✅ 이름 입력
name = st.text_input("👤 학생 이름:", key="name_input")

if not name:
    st.stop()

filename = f"wrong_words_{name}.txt"
if not os.path.exists(filename):
    st.warning("⚠️ 오답 파일이 없습니다.")
    st.stop()

# ✅ 날짜 범위 선택
date_option = st.radio("📅 복습할 기간:", ["오늘", "최근 3일", "최근 7일", "전체"], horizontal=True)

# ✅ 날짜 필터링 함수
def filter_by_date(line):
    if date_option == "전체":
        return True
    try:
        line_date = datetime.strptime(line.strip()[1:17], "%Y-%m-%d %H:%M")
        now = datetime.now()
        if date_option == "오늘":
            return line_date.date() == now.date()
        elif date_option == "최근 3일":
            return line_date >= now - timedelta(days=3)
        elif date_option == "최근 7일":
            return line_date >= now - timedelta(days=7)
    except:
        return False

# ✅ 오답 불러오기
with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

questions = []
i = 0
while i < len(lines):
    if lines[i].startswith("[") and filter_by_date(lines[i]):
        word = lines[i+1].split(":")[1].strip()
        wrong = lines[i+2].split("/")[0].split(":")[1].strip()
        correct = lines[i+2].split("/")[-1].split(":")[1].strip()
        questions.append({"word": word, "correct": correct, "wrong": wrong})
        i += 4
    else:
        i += 1

if not questions:
    st.info("📭 선택한 기간에 오답 기록이 없습니다.")
    st.stop()

# ✅ 퀴즈 진행
st.markdown("## 🧾 복습 퀴즈")

deleted = []

for idx, q in enumerate(questions):
    st.markdown(f"### {idx+1}. `{q['word']}`")

    options = [q["correct"]]
    while len(options) < 4:
        dummy = random.choice(questions)["correct"]
        if dummy not in options:
            options.append(dummy)
    random.shuffle(options)

    selected = st.radio("뜻을 고르세요:", options, index=None, key=f"quiz_{idx}", horizontal=True)

    if selected:
        if selected == q["correct"]:
            st.success("✅ 정답입니다!")
            if st.checkbox("🗑️ 복습 완료 – 삭제", key=f"del_{idx}"):
                deleted.append(q["word"])
        else:
            st.error(f"❌ 오답입니다. 정답: `{q['correct']}`")

    st.markdown("---")

# ✅ 삭제 처리
if deleted:
    if st.button("🧹 복습 완료 단어 삭제하기"):
        new_lines = []
        skip = False
        for line in lines:
            if any(word in line for word in deleted):
                skip = True
            elif skip and line.strip() == "-" * 30:
                skip = False
                continue
            if not skip:
                new_lines.append(line)
        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        st.success("✅ 삭제 완료! 새로고침 후 반영됩니다.")
