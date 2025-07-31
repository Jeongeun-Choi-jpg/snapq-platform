# pages/word_review_quiz.py

import streamlit as st
import random
import os
from datetime import datetime

st.set_page_config(page_title="🧠 단어 복습 퀴즈", layout="centered")
st.title("🧠 단어 복습 퀴즈")
st.markdown("#### 복습할 이름을 입력하고 퀴즈를 풀어보세요!")

# ✅ 이름 입력
name = st.text_input("👤 이름을 입력하세요:", key="name_input")

if not name:
    st.stop()

filename = f"wrong_words_{name}.txt"
if not os.path.exists(filename):
    st.warning("⚠️ 해당 이름의 오답 기록 파일이 없습니다.")
    st.stop()

# ✅ 오답 데이터 파싱
with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

questions = []
i = 0
while i < len(lines):
    if lines[i].startswith("["):
        word = lines[i+1].split(":")[1].strip()
        wrong = lines[i+2].split("/")[0].split(":")[1].strip()
        correct = lines[i+2].split("/")[-1].split(":")[1].strip()
        questions.append({"word": word, "correct": correct, "wrong": wrong})
        i += 4
    else:
        i += 1

if not questions:
    st.info("✅ 오답 기록이 없습니다.")
    st.stop()

# ✅ 퀴즈 표시
st.markdown("## ✏️ 오답 단어 퀴즈 시작!")
score = 0
deleted = []

for idx, q in enumerate(questions):
    st.markdown(f"### {idx+1}. `{q['word']}`")
    
    options = [q["correct"]]
    while len(options) < 4:
        dummy = random.choice(questions)["correct"]
        if dummy not in options:
            options.append(dummy)
    random.shuffle(options)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("📌 선택지:")
    with col2:
        selected = st.radio(
            "", options, index=None, key=f"quiz_{idx}", horizontal=True
        )

    if selected:
        if selected == q["correct"]:
            st.success("✅ 정답입니다!")
            if st.checkbox("🗑️ 복습 완료 – 삭제", key=f"del_{idx}"):
                deleted.append(q["word"])
        else:
            st.error(f"❌ 오답입니다! 정답은 `{q['correct']}` 입니다.")

    st.markdown("---")

# ✅ 복습 완료 단어 삭제
if deleted:
    if st.button("🧹 복습 완료된 단어 삭제하기"):
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
