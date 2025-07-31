import streamlit as st
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

# 📌 PDF 생성 함수
def generate_pdf(name, wrong_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"{name}님의 단어 복습 리포트", ln=True, align='C')
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)

    for i, item in enumerate(wrong_data, 1):
        pdf.cell(200, 10, txt=f"{i}. 단어: {item['word']}", ln=True)
        pdf.cell(200, 10, txt=f"   내가 고른 답: {item['user_answer']}", ln=True)
        pdf.cell(200, 10, txt=f"   정답: {item['correct_answer']}", ln=True)
        pdf.cell(200, 5, txt="   -------------------------", ln=True)

    file_name = f"{name}_report.pdf"
    pdf.output(file_name)
    return file_name

# 📌 이메일 전송 함수
def send_email(receiver_email, pdf_file, name):
    sender_email = "your_email@gmail.com"  # ✅ 본인의 Gmail
    sender_password = "your_app_password"  # ✅ Gmail 앱 비밀번호 (2단계 인증 필요)

    msg = EmailMessage()
    msg['Subject'] = f"{name}님의 단어 복습 리포트"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(f"{name}님의 복습 결과가 첨부되어 있습니다. 확인해 주세요.")

    with open(pdf_file, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=pdf_file)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

# ✅ Streamlit UI
st.title("📤 단어 복습 리포트 전송")
name = st.text_input("🧒 이름을 입력하세요")
email = st.text_input("📧 이메일 주소를 입력하세요")

# 예시 오답 데이터 (실제에선 자동 수집 가능)
sample_wrong_data = [
    {"word": "apple", "user_answer": "banana", "correct_answer": "apple"},
    {"word": "grape", "user_answer": "peach", "correct_answer": "grape"},
]

if st.button("📄 PDF 생성 및 이메일 발송"):
    if name and email:
        with st.spinner("리포트를 생성하고 이메일을 보내는 중입니다..."):
            pdf_path = generate_pdf(name, sample_wrong_data)
            send_email(email, pdf_path, name)
            os.remove(pdf_path)  # 전송 후 삭제
        st.success("📩 이메일 전송 완료!")
    else:
        st.warning("이름과 이메일을 모두 입력하세요.")
