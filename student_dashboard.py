# student_dashboard.py

import streamlit as st

st.set_page_config(page_title="📚 SnapQ 학생 대시보드", layout="centered")
st.title("📚 SnapQ 학생 대시보드")
st.markdown("### 안녕하세요! 원하시는 메뉴를 선택하세요 😊")
st.markdown("---")

# ✅ 메뉴 버튼
menu = st.radio(
    "📌 메뉴 선택",
    ("🧠 단어 복습 퀴즈", "📆 오답 리마인드 복습"),
    index=0,
)

# ✅ 각 메뉴 연결
if menu == "🧠 단어 복습 퀴즈":
    st.markdown("➡️ 오른쪽 상단 메뉴에서 `▶ word_review_quiz` 페이지로 이동하세요.")
elif menu == "📆 오답 리마인드 복습":
    st.markdown("➡️ 오른쪽 상단 메뉴에서 `▶ remind_wrong_words` 페이지로 이동하세요.")

st.markdown("---")
st.info("💡 이 대시보드는 SnapQ의 학생용 기능을 한 곳에 모은 메인 메뉴입니다.")
