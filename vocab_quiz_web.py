import streamlit as st
import random

SAMPLE_DICTIONARY = {
    "media": "미디어",
    "connect": "연결하다",
    "share": "공유하다",
    "compare": "비교하다",
    "change": "변화시키다",
    "global": "세계적인",
    "anxiety": "불안",
    "moment": "순간",
    "platform": "플랫폼",
    "problem": "문제",
    "solution": "해결책",
    "think": "생각하다",
    "create": "창조하다",
    "student": "학생",
    "research": "연구하다",
    "present": "발표하다"
}

def load_vocab_words(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    words = [line.strip() for line in lines if line.strip() and not line.startswith("[") and not line.startswith("-")]
    return list(set(words))

def generate_choices(correct_word, all_words):
    correct_meaning = SAMPLE_DICTIONARY.get(correct_word)
    other_meanings = [v for k, v in SAMPLE_DICTIONARY.items() if k != correct_word and v != correct_meaning]
    wrong_choices = random.sample(other_meanings, 3)
    choices = wrong_choices + [correct_meaning]
    random.shuffle(choices)
    return choices, correct_meaning

# -------- Streamlit UI --------
st.set_page_config(page_title="SnapQ 단어 객관식 퀴즈", layout="wide")
st.title("🎯 SnapQ 단어 복습 퀴즈 (4지선다형)")

with st.sidebar:
    user_name = st.text_input("이름을 입력하세요", "").strip().lower()
    start_button = st.button("🔁 객관식 퀴즈 시작")

if start_button:
    if not user_name:
        st.warning("이름을 입력하세요.")
        st.stop()

    filename = f"vocab_log_{user_name}.txt"
    vocab_words = load_vocab_words(filename)

    if not vocab_words:
        st.error("❌ 저장된 단어가 없습니다.")
        st.stop()

    quiz_words = [w for w in vocab_words if w in SAMPLE_DICTIONARY]
    if not quiz_words:
        st.warning("⚠️ 저장된 단어 중 의미가 등록된 단어가 없습니다.")
        st.stop()

    selected_words = random.sample(quiz_words, min(10, len(quiz_words)))
    st.success(f"✅ 총 {len(selected_words)}개의 단어 퀴즈가 준비되었습니다!")

    score = 0
    for idx, word in enumerate(selected_words):
        choices, correct_meaning = generate_choices(word, vocab_words)
        with st.form(f"form_{idx}"):
            st.markdown(f"**Q{idx+1}. {word}** 의 뜻으로 알맞은 것은?")
            choice = st.radio("선택하세요:", choices, key=f"radio_{idx}")
            submitted = st.form_submit_button("정답 확인")

            if submitted:
                if choice == correct_meaning:
                    st.success("✅ 정답입니다!")
                    score += 1
                else:
                    st.error(f"❌ 오답입니다! 정답: {correct_meaning}")

    st.markdown("---")
    st.subheader("📊 퀴즈 결과 요약")
    st.markdown(f"- 총 문제 수: **{len(selected_words)}**")
    st.markdown(f"- 맞힌 개수: **{score}**")
    st.markdown(f"- 정답률: **{round((score/len(selected_words))*100, 1)}%**")
