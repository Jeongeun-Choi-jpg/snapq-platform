import time
import re
from reading_passages import get_passage

# 불용어 (중복 제외 대상, 필요시 확장 가능)
STOPWORDS = {"the", "and", "a", "an", "in", "on", "at", "for", "to", "of", "is", "are", "was", "were", "with", "that", "this", "it", "as", "by", "be"}

def is_duplicate_question(question_text, filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            return question_text in content
    except FileNotFoundError:
        return False

def save_wrong_answer(theme, level, question_type, question, options, user_answer, correct_answer, filename):
    if is_duplicate_question(question, filename):
        print("⚠️ 이미 저장된 오답입니다. 중복 저장하지 않습니다.")
        return

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{theme} - Lv{level}]\n")
        f.write(f"❌ 문제 유형: {question_type}\n")
        f.write(f"Q: {question}\n")
        f.write(f"보기: {' / '.join(options)}\n")
        f.write(f"내 답: {user_answer}\n")
        f.write(f"정답: {correct_answer}\n")
        f.write("------------------------\n")

def extract_keywords(paragraphs):
    text = " ".join(paragraphs).lower()
    words = re.findall(r'\b[a-z]{3,}\b', text)  # 알파벳 3글자 이상 단어만 추출
    keywords = [w for w in words if w not in STOPWORDS]
    return sorted(set(keywords))

def save_keywords_to_file(user_name, theme, level, keywords):
    filename = f"vocab_log_{user_name}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{theme} - Lv{level}]\n")
        for word in keywords:
            f.write(word + "\n")
        f.write("------------------------\n")

def main():
    user_name = input("사용자 이름을 입력하세요: ").strip().lower()
    if not user_name:
        print("사용자 이름은 필수입니다.")
        return

    wrong_log_file = f"wrong_log_{user_name}.txt"
    vocab_file = f"vocab_log_{user_name}.txt"

    theme = input("지문 범주를 입력하세요 (예: 사회·문화): ").strip()
    level = input("레벨을 입력하세요 (1~5): ").strip()

    try:
        level_int = int(level)
    except ValueError:
        print("레벨은 숫자여야 합니다.")
        return

    try:
        passage_data = get_passage(theme, level_int)
    except KeyError:
        print("해당 범주나 레벨에 맞는 지문이 없습니다.")
        return

    paragraphs = passage_data["paragraphs"]
    questions_by_progress = passage_data["questions_by_progress"]

    print(f"\n📖 {user_name}님, 지문을 읽어주세요 (제한 시간 60초)")
    print("-" * 40)
    for p in paragraphs:
        print(p)
    print("-" * 40)

    # 단어 추출 및 저장
    keywords = extract_keywords(paragraphs)
    save_keywords_to_file(user_name, theme, level, keywords)

    time.sleep(3)  # 실제 사용 시 60초로 변경 가능

    score = 0
    for idx in range(len(questions_by_progress)):
        qdata = questions_by_progress[idx]
        print(f"\n문제 {idx + 1}: {qdata['question']}")
        for i, opt in enumerate(qdata["options"], 1):
            print(f"{i}. {opt}")

        try:
            user_input = int(input("당신의 선택 (번호 입력): "))
            user_choice = qdata["options"][user_input - 1]
        except (ValueError, IndexError):
            print("⚠️ 잘못된 입력입니다. 틀린 것으로 처리됩니다.")
            user_choice = None

        if user_choice == qdata["answer"]:
            print("✅ 정답입니다!")
            score += 1
        else:
            print(f"❌ 오답입니다! 정답: {qdata['answer']}")
            save_wrong_answer(
                theme=theme,
                level=level,
                question_type=qdata.get("type", "unknown"),
                question=qdata["question"],
                options=qdata["options"],
                user_answer=user_choice,
                correct_answer=qdata["answer"],
                filename=wrong_log_file
            )

    print(f"\n📝 {user_name}님의 총 점수: {score} / {len(questions_by_progress)}")

if __name__ == "__main__":
    main()
