# generate_report.py

import streamlit as st
from fpdf import FPDF
import os
import re
from datetime import datetime

st.set_page_config(page_title="📄 리포트 생성", layout="centered")
st.title("📤 학생별 리포트 PDF 생성기")

# 👤 이름 입력
name = st.text_input("🧒 학생 이름을 입력하세요:")
if not name:
    st.stop()

log_path = f"result_log_{name}.txt"
if not os.path.exists(log_path):
    st.warning("📁 복습 기록 파일이 없습니다.")
    st.stop()

# 📖 최근 결과 추출
with open(log_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

if not lines:
    st.info("📌 기록이 없습니다.")
    st.stop()

latest = lines[-1]
match = re.search(r"정답: (\d+)/(\d+), 정답률: ([\d.]+)%", latest)
if match:
    correct = int(match.group(1))
    total = int(match.group(2))
    acc = float(match.group(3))
else:
    st.error("❌ 로그 형식이 올바르지 않습니다.")
    st.stop()

# 🧾 PDF 생성
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, f"[SnapQ 단어 복습 리포트]", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, f"🧒 이름: {name}", ln=True)
pdf.cell(0, 10, f"📅 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
pdf.cell(0, 10, f"✅ 최근 정답 수: {correct} / {total}", ln=True)
pdf.cell(0, 10, f"📊 최근 정답률: {acc:.1f}%", ln=True)

filename = f"report_{name}.pdf"
pdf.output(filename)

with open(filename, "rb") as f:
    st.download_button("📥 리포트 PDF 다운로드", f, file_name=filename)

st.success("✅ PDF 리포트가 생성되었습니다!")
