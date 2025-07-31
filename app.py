# app.py

import streamlit as st

st.set_page_config(page_title="📘 SnapQ - 영어 독해 플랫폼", layout="centered")

# 🎨 페이지 상단 제목
st.title("📘 SnapQ 영어 독해 & 복습 플랫폼")
st.markdown("---")

# 🧭 메뉴 선택
mode = st.sidebar.selectbox("🔍 모드 선택", ["학생용 메뉴", "관리자용 메뉴"])

if mode == "학생용 메뉴":
    st.subheader("🧒 학생용 기능 안내")
    st.markdown("""
    - 🧠 **단어 복습 퀴즈**: 오답 단어를 4지선다 객관식으로 복습합니다.  
    - 📆 **오답 날짜 복습**: 최근 오답을 날짜 기준으로 다시 풀어볼 수 있습니다.  
    - 📈 **단어 통계 확인** (선택): 복습 정답률을 그래프로 확인합니다.
    """)

    st.markdown("👉 왼쪽 사이드바에서 기능을 선택하세요.")

elif mode == "관리자용 메뉴":
    st.subheader("👨‍🏫 관리자용 기능 안내")
    st.markdown("""
    - 📊 **학생별 성취 분석**: 오답 기록을 기반으로 그래프 제공  
    - 📤 **PDF + 이메일 자동 전송**: 학생 오답 리포트를 메일로 보냅니다.
    """)

    st.markdown("👉 왼쪽 사이드바에서 기능을 선택하세요.")

# 📌 공통 안내
st.markdown("---")
st.markdown("🚀 **모든 기능은 좌측 사이드바에서 선택할 수 있습니다.**")
st.markdown("🔒 관리자 기능은 개인정보 보호를 위해 이메일/비밀번호 입력이 필요합니다.")
