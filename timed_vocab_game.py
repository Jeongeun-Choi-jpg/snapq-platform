from reading_passages import get_passage
import random

def extract_vocab(paragraphs):
    words = set()
    for line in paragraphs:
        for word in line.split():
            cleaned = word.strip(".,!?\"'()").lower()
            if cleaned.isalpha() and len(cleaned) > 4:
                words.add(cleaned)
    return list(words)

def vocab_quiz(vocab_list):
    print("\n📚 [어휘 퀴즈 시작]")
    for i in range(min(5, len(vocab_list))):
        word = random.choice(vocab_list)
        print(f"단어: {word}")
        input("이 단어의 뜻을 적어보세요 (Enter 입력 시 다음): ")

def run_vocab_mode():
    theme = input("테마를 입력하세요 (예: 사회·문화): ").strip()
    level = input("레벨을 입력하세요 (1~5): ").strip()

    if not level.isdigit():
        print("❌ 숫자만 입력하세요.")
        return

    index = int(level) - 1
    try:
        passage = get_passage(theme, index)
        vocab_list = extract_vocab(passage["paragraphs"])
        if not vocab_list:
            print("❗ 어휘가 충분하지 않습니다.")
            return
        vocab_quiz(vocab_list)
    except Exception as e:
        print("⚠ 오류:", e)

if __name__ == "__main__":
    run_vocab_mode()
