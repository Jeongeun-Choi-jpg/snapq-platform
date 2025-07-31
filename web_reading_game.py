import streamlit as st
import random
import time
from reading_passages import get_passage
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="SnapQ 독해 연습", layout="centered")

# 헤더
st.title("📘 SnapQ 독해 연습")
st.markdown("**🧠 오늘의 실력을 테스트해보세요!**")

# 테마 & 레벨 선택
theme = st.selectbox("📚 지문 범주 선택", [
    "사회·문화", "과학 일반", "기술·공학", "건강·의학", "환경",
    "심리학", "경제·비즈니스", "교육", "예술", "역사",
    "정치·법", "스포츠", "윤리·철학", "여행·지리", "미래사회·직업"
])

level = st.slider("📈 난이도 (Lv1 ~ Lv5)", 1, 5, 1)

# 사용자 이름 입력
username = st.text_input("👤 이름을 입력하세요", key="username")

if theme and level and username:
    # 지문 데이터 가져오기
    data = get_passage(theme, level)
    paragraphs = data["paragraphs"]
    questions_by_progress = data["questions_by_progress"]

    # 상태 초기화
    if "progress" not in st.session_state:
        st.session_state.progress = 0
        st.session_state.score = 0
        st.session_state.vocab_log = []
        st.session_state.wrong_log = []

    progress = st.session_state.progress

    if progress < len(paragraphs):
        # 진행 중일 때: 문단 보여주기
        with st.container():
            st.markdown(f"### ✨ 문단 {progress + 1}")
            st.markdown(f"<div style='background-color:#f0f2f6;padding:15px;border-radius:10px;'>{paragraphs[progress]}</div>", unsafe_allow_html=True)

        st.button("다음", key=f"next_{progress}", on_click=lambda: st.session_state.update({"progress": progress + 1}))
    else:
        # 문제 출제
        question_data = questions_by_progress.get(progress - 1)
        if question_data:
            q = question_data["question"]
            options = question_data["options"]
            answer = question_data["answer"]
            q_type = question_data.get("type", "unknown")

            st.markdown("### ❓ 문제")
            st.markdown(f"**{q}**")

            user_choice = st.radio("👉 보기 선택", options, key=f"q_{progress}")

            if st.button("정답 확인", key=f"submit_{progress}"):
                if user_choice == answer:
                    st.success("✅ 정답입니다!")
                    st.session_state.score += 1
                else:
                    st.error("❌ 오답입니다!")
                    wrong_entry = f"[{theme} - Lv{level}]\n❌ 문제 유형: {q_type}\nQ: {q}\n내 답: {user_choice}\n정답: {answer}\n------------------------\n"
                    st.session_state.wrong_log.append(wrong_entry)

                # 단어 추출
                wrong_words = [word for word in answer.split() if word.istitle()]
                st.session_state.vocab_log.extend(wrong_words)

                st.session_state.progress += 1
                st.experimental_rerun()
        else:
            # 최종 결과
            st.markdown("## 🎉 테스트 완료!")
            st.markdown(f"✅ 최종 점수: **{st.session_state.score} / {len(paragraphs)}**")

            # 오답 저장
            if st.session_state.wrong_log:
                wrong_path = f"wrong_log_{username}.txt"
                with open(wrong_path, "a", encoding="utf-8") as f:
                    f.write("\n".join(st.session_state.wrong_log))

            # 단어 저장
            if st.session_state.vocab_log:
                vocab_path = f"vocab_log_{username}.txt"
                with open(vocab_path, "a", encoding="utf-8") as f:
                    for word in st.session_state.vocab_log:
                        f.write(word + "\n")

            st.button("🔁 다시 시작하기", on_click=lambda: st.session_state.clear())
