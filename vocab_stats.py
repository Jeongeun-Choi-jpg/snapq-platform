# vocab_stats.py

import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import re
import os

st.set_page_config(page_title="📊 복습 통계 보기", layout="centered")

st.title("📈 학생별 단어 복습 통계")

name = st.text_input("🧒 이름을 입력하세요:")
if not name:
    st.stop()

log_path = f"result_log_{name}.txt"

if not os.path.exists(log_path):
    st.warning("📂 결과 로그 파일이 없습니다. 먼저 퀴즈를 진행해주세요.")
    st.stop()

# ✅ 로그 읽기
with open(log_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

if not lines:
    st.info("🔎 아직 기록된 복습 결과가 없습니다.")
    st.stop()

dates = []
scores = []
accuracies = []

# 날짜가 없을 경우 임의 순번 부여
for idx, line in enumerate(lines):
    match = re.search(r"정답: (\d+)/(\d+), 정답률: ([\d.]+)%", line)
    if match:
        correct = int(match.group(1))
        total = int(match.group(2))
        acc = float(match.group(3))
        dates.append(f"{idx+1}회차")
        scores.append((correct, total))
        accuracies.append(acc)

# 📊 정답률 그래프
st.subheader("📊 정답률 변화 추이")
fig, ax = plt.subplots()
ax.plot(dates, accuracies, marker='o', linestyle='-', color='blue')
ax.set_xlabel("회차")
ax.set_ylabel("정답률 (%)")
ax.set_ylim(0, 100)
ax.grid(True)
st.pyplot(fig)

# 📈 누적 통계
total_quizzes = len(scores)
total_questions = sum(t for c, t in scores)
total_correct = sum(c for c, t in scores)
average_accuracy = sum(accuracies) / len(accuracies)

st.subheader("📋 누적 통계")
st.write(f"🔢 총 퀴즈 수: {total_quizzes}회")
st.write(f"✅ 총 정답 수: {total_correct} / {total_questions}")
st.write(f"📌 평균 정답률: {average_accuracy:.1f}%")
