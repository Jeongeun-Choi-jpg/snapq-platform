import streamlit as st
import random
from reading_passages import get_passage

if "theme" not in st.session_state:
    st.session_state.theme = ""
if "level" not in st.session_state:
    st.session_state.level = 1
if "passage" not in st.session_state:
    st.session_state.passage = None
if "progress" not in st.session_state:
    st.session_state.progress = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

LEVEL_SCORE = {
    1: 10,
    2: 20,
    3: 30,
    4: 40,
    5: 50
}

def load_new_passage():
    theme = st.session_state.theme
    level = st.session_state.level
    st.session_state.passage = get_passage(theme, level)
    st.session_state.progress = 0
    st.session_state.question_count = 0

st.title("📘 독해 누적 게임 (Lv별 점수 시스템)")

themes = ["사회·문화", "과학 일반", "기술·공학", "건강·의학", "환경", "심리학", "경제·비즈니스", "교육", "예술", "역사", "정치·법", "스포츠", "윤리·철학", "여행·지리", "미래사회·직업"]
theme = st.selectbox("지문 범주 선택", themes)
level = st.slider("레벨 선택 (1~5)", 1, 5, st.session_state.level)

if theme != st.session_state.theme or level != st.session_state.level:
    st.session_state.theme = theme
    st.session_state.level = level
    load_new_passage()
    st.session_state.score = 0

if st.session_state.passage:
    max_index = [2, 5, 8][min(st.session_state.progress, 2)]
    for i in range(max_index):
        if i < len(st.session_state.passage["paragraphs"]):
            st.write(st.session_state.passage["paragraphs"][i])

    q_data = st.session_state.passage["questions_by_progress"].get(st.session_state.progress)
    if q_data:
        st.subheader(f"문제 {st.session_state.question_count + 1}")
        user_answer = st.radio(q_data["question"], q_data["options"], key=st.session_state.question_count)

        if st.button("제출하기", key=f"submit_{st.session_state.question_count}"):
            if user_answer == q_data["answer"]:
                st.success("정답입니다!")
                st.session_state.progress += 1
                st.session_state.score += LEVEL_SCORE[st.session_state.level]
            else:
                st.error("오답입니다.")
            st.session_state.question_count += 1

    if st.session_state.progress >= 3:
        st.success("문제를 모두 맞추셨어요! 다음 지문으로 넘어갑니다.")
        st.write(f"🎯 **이번 지문 점수: {LEVEL_SCORE[st.session_state.level] * 3}점**")
        st.write(f"🏆 **누적 점수: {st.session_state.score}점**")
        if st.button("다음 지문으로 이동"):
            load_new_passage()
