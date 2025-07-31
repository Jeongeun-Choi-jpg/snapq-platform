# wrong_vocab_quiz.py

import streamlit as st
import random
import os

# 🎯 단어-뜻 사전
word_dict = {
    "apple": "사과",
    "banana": "바나나",
    "grape": "포도",
    "orange": "오렌지",
    "peach": "복숭아",
    "melon": "멜론",
    "lemon": "레몬",
    "mango": "망고"
}

# 🧑 사용자 이름 입력
name = st.text_input("🧒 이름을 입력하세요:")
if not name:
    st.stop()

# 📁 오답 단어 경로
wrong_path = f"wrong_vocab_{name}.txt"

# 🧾 오답 단어 불러오기
try:
    with open(wrong_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    st.warning("❗ 오답 복습 단어가 없습니다.")
    st.stop()

if not words:
    st.info("👏 모든 오답을 복습 완료했어요!")
    st.stop()

# 🔄 단어 섞기
random.shuffle(words)
quiz_words = words[:5]

st.markdown("## ❗ 오답 복습 퀴즈 (객관식)")
st.write(f"현재 오답 단어 수: {len(words)}개 중 {len(quiz_words)}개 복습")

score = 0
remove_list = []  # 맞히고 체크된 단어들만 삭제

for idx, word in enumerate(quiz_words):
    correct = word_dict.get(word)
    if not correct:
        continue

    all_choices = list(set(word_dict.values()) - {correct})
    options = random.sample(all_choices, 3) + [correct]
    random.shuffle(options)

    st.markdown(f"### Q{idx+1}. '{word}'의 뜻은?")
    choice = st.radio("정답을 고르세요:", options, key=f"q{idx}")

    if st.button("정답 확인", key=f"submit{idx}"):
        if choice == correct:
            st.success("✅ 정답입니다!")
            score += 1
            if st.checkbox("🧹 이 단어를 오답 목록에서 삭제할까요?", key=f"chk{idx}"):
                remove_list.append(word)
        else:
            st.error(f"❌ 오답입니다. 정답은: {correct}")

# 결과 보기 버튼
if st.button("최종 결과 보기"):
    total = len(quiz_words)
    accuracy = (score / total) * 100
    st.write(f"🎯 정답률: {accuracy:.1f}%  ({score} / {total})")

    # 삭제할 단어 반영
    if remove_list:
        updated_words = [w for w in words if w not in remove_list]
        with open(wrong_path, "w", encoding="utf-8") as f:
            for w in updated_words:
                f.write(w + "\n")
        st.success(f"🧽 {len(remove_list)}개 단어가 오답 목록에서 삭제되었습니다.")

    else:
        st.info("❕ 삭제된 단어는 없습니다.")
