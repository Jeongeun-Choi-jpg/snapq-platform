import random

# 단어 뜻을 임시로 담은 샘플 사전
sample_dictionary = {
    "benefit": "이익",
    "effort": "노력",
    "analyze": "분석하다",
    "average": "평균",
    "participate": "참여하다",
    "emotion": "감정",
    "result": "결과",
    "behavior": "행동",
    "issue": "문제",
    "advocate": "지지하다",
    "regulate": "규제하다",
    "imply": "암시하다",
    "obscure": "모호한",
    "tentative": "잠정적인",
    "paradox": "역설"
}

def generate_quiz_words(word_list):
    quiz_set = []

    for word in word_list:
        if word not in sample_dictionary:
            continue  # 뜻 모르면 건너뜀

        correct_meaning = sample_dictionary[word]
        wrong_meanings = list(sample_dictionary.values())
        wrong_meanings.remove(correct_meaning)
        distractors = random.sample(wrong_meanings, 3)  # 오답 3개 선택
        options = [correct_meaning] + distractors
        random.shuffle(options)

        quiz_set.append({
            "word": word,
            "answer": correct_meaning,
            "options": options
        })

    return quiz_set
