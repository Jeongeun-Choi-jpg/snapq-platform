import streamlit as st
import os
import subprocess

st.set_page_config(page_title="🔥 SnapQ 게임 허브", layout="centered")

st.title("🎮 SnapQ 게임 허브")
st.markdown("---")

st.header("🧩 모드 선택")
mode = st.radio("원하는 미션을 선택하세요!", ["🔍 무기부터 챙긴다 (단어 정찰전)", "⚔️ 바로 전장 돌입한다 (독해 미션)"])

if st.button("🚀 미션 시작하기"):
    if mode.startswith("🔍"):
        subprocess.Popen(["python", "random_vocab_quiz.py"], shell=True)
        st.success("단어 정찰전을 시작합니다! 🔍")
    elif mode.startswith("⚔️"):
        subprocess.Popen(["python", "timed_reading_game_ui.py"], shell=True)
        st.success("전장에 돌입합니다! ⚔️")

st.markdown("---")
st.subheader("📕 나의 비밀무기 리스트 보기")
if st.button("📘 무기 리스트 열기"):
    subprocess.Popen(["python", "secret_word_list.py"], shell=True)
    st.info("무기 리스트 창이 열렸습니다!")

st.subheader("📊 단어 정답률 그래프")
if st.button("📈 그래프 열기"):
    subprocess.Popen(["python", "quiz_stats_graph.py"], shell=True)
    st.info("정답률 그래프 창이 열렸습니다!")

st.subheader("🧽 비밀무기 리스트 정리하기")
if st.button("🧹 무기 청소 시작"):
    subprocess.Popen(["python", "secret_weapon_cleaner.py"], shell=True)
    st.warning("무기 청소 창이 열렸습니다!")

st.markdown("---")
st.button("🚪 종료하기")
