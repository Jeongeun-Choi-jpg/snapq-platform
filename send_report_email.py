import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os

def send_report(username, receiver_email, sender_email, sender_password):
    report_path = f"report_{username}.pdf"
    if not os.path.exists(report_path):
        raise FileNotFoundError(f"리포트 PDF가 존재하지 않습니다: {report_path}")

    # 이메일 설정
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = f"[SnapQ] {username}님의 학습 리포트"

    # 본문 텍스트
    body = MIMEText(f"""
안녕하세요, {username}님의 SnapQ 학습 리포트를 첨부드립니다.

- 오답 복습 현황
- 주요 단어 정리
- 최근 3개 오답

감사합니다.
""", _charset="utf-8")
    msg.attach(body)

    # PDF 첨부
    with open(report_path, "rb") as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
        pdf_attachment.add_header("Content-Disposition", "attachment", filename=report_path)
        msg.attach(pdf_attachment)

    # SMTP 설정 (Gmail 예시)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print(f"✅ 이메일 전송 완료: {receiver_email}")
