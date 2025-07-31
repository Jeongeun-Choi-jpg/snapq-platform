import streamlit as st
from datetime import datetime, timedelta
import os
import random
import re

# 설정
st.set_page_config(page_title="📆 SnapQ 오답 복습", layout="centered")
st.title("📆 오답 복습 자동화")
st.markdown("**📚 최근 오답을 자동으로 불러와서 다시 풀어보세요!**")

# 사용자 이름 입력
username = st.text_input("👤 이름을 입력하세요", key="username_input")

if username:
    filename = f"wrong_log_{username}.txt"
    if not os.path.exists(filename):
        st.warning("❌ 오답 기록이 없습니다.")
        st.stop()

    # 오답 파일 읽기
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # 오답 블록으로 나누기
    blocks = content.strip().split("------------------------")
    review_items = []

    # 날짜 기준 필터링
    today = datetime.now().date()
    review_day = today - timedelta(days=3)

    for block in blocks:
        if not block.strip():
            continue

        try:
            theme = re.search(r"\[(.+?) - Lv\d\]", block).group(1)
            q_type = re.search(r"문제 유형: (.+)", block).group(1)
            question = re.search(r"Q: (.+)", block).group(1)
            user_answer = re.search(r"내 답: (.+)", block).group(1)
            correct_answer = re.search(r"정답: (.+)", block).group(1)
            date_str = re.search(r"📅 날짜: (\d{4}-\d{2}-\d{2})", block).group(1)
            log_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            if log_date == review_day:
                # 객관식 보기를 생성 (정답 + 사용자 답 + 랜덤 오답)
                distractors = ["Apple", "Banana", "Fish", "Bread", "Soup", "Chicken", "Egg"]
                options = list(set([correct_answer, user_answer] + random.sample(distractors, 2)))
                random.shuffle(options)

                review_items.append({
                    "theme": theme,
                    "question": question,
                    "options": options,
                    "answer": correct_answer
                })
        except Exception as e:
            continue

    if not review_items:
        st.info(f"📅 {review_day.strftime('%Y-%m-%d')} 기준 복습할 오답이 없습니다.")
        st.stop()

    st.markdown(f"### 🧠 복습 대상: {len(review_items)}개")
    st.markdown("**3일 전 오답 복습입니다. 아래 문제를 다시 풀어보세요!**")
    st.divider()

    for idx, item in enumerate(review_items):
        st.markdown(f"**{idx+1}. {item['question']}**")
        choice = st.radio("선택:", item["options"], key=f"review_{idx}")

        if st.button("정답 확인", key=f"submit_review_{idx}"):
            if choice == item["answer"]:
                st.success("🎉 정답입니다! 복습 성공!")
            else:
                st.error(f"❌ 오답입니다. 정답: {item['answer']}")

        st.divider()
