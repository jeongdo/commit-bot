# step-03_learning_mapper.py
class Brain:
    def __init__(self):
        # 각 한글 단어 → (영어 후보, 가중치) 리스트
        self.candidates = {
            "추가": [("add", 0.9), ("insert", 0.1)],
            "수정": [("fix", 0.8), ("modify", 0.2)],
            "삭제": [("remove", 0.7), ("delete", 0.3)],
            "버그": [("bug", 1.0)],
            "로그인": [("login", 1.0)],
            "회원가입": [("signup", 0.9), ("register", 0.1)],
        }
        self.learning_rate = 0.1  # 학습 속도 (한 번에 얼마나 바꿀지)

    def think(self, sentence: str) -> str:
        """입력 문장을 영어로 변환"""
        words = sentence.strip().split()
        result_parts = []
        self.last_input_words = words  # 학습을 위해 기억
        self.last_selected = []  # 어떤 후보를 골랐는지 기억

        for w in words:
            if w in self.candidates:
                best = max(self.candidates[w], key=lambda pair: pair[1])
                result_parts.append(best[0])
                self.last_selected.append((w, best))
            else:
                result_parts.append(w)
                self.last_selected.append((w, None))

        return ' '.join(result_parts)

    def learn(self, correct_sentence: str):
        """
        정답 문장을 보고 가중치를 조정함
        예: learn("login insert")  # "추가"를 "insert"로 번역하길 원함
        """
        correct_words = correct_sentence.strip().split()

        for i, (original_word, selected) in enumerate(self.last_selected):
            if i >= len(correct_words):
                break

            correct_word = correct_words[i]

            # 모르는 단어면 스킵
            if selected is None or original_word not in self.candidates:
                continue

            # 선택된 단어가 정답과 다른 경우
            if selected[0] != correct_word:
                # 틀린 선택의 가중치 낮춤
                self._decrease_weight(original_word, selected[0])

                # 정답 후보가 있으면 가중치 높임
                self._increase_weight(original_word, correct_word)

    def _decrease_weight(self, word, wrong_translation):
        """틀린 번역의 가중치를 낮춤"""
        for i, (trans, weight) in enumerate(self.candidates[word]):
            if trans == wrong_translation:
                new_weight = weight - self.learning_rate
                self.candidates[word][i] = (trans, max(0.01, new_weight))
                break

    def _increase_weight(self, word, correct_translation):
        """맞는 번역의 가중치를 높임"""
        for i, (trans, weight) in enumerate(self.candidates[word]):
            if trans == correct_translation:
                new_weight = weight + self.learning_rate
                self.candidates[word][i] = (trans, min(0.99, new_weight))
                break
        else:
            # 정답 후보가 아예 없으면 새로 추가
            self.candidates[word].append((correct_translation, 0.5))


# 테스트
if __name__ == "__main__":
    brain = Brain()

    print("=== 학습 전 ===")
    print(brain.think("추가"))  # "add"
    print(brain.candidates["추가"])  # 단순 기존 가중치 결과를 보는 것 : [("add", 0.9), ("insert", 0.1)]

    brain.think("추가")  # 먼저 생각하게 하고, 여전히 add 나오고, 기억해둔 답안지

    print("\n=== 학습: '추가' → 'insert' 라고 알려줌 ===")
    brain.learn("insert")  # 정답이 "insert"라고 알려줌, 채점하면서 틀린 부분 수정
    print("\n=== 학습 후 ===")
    print(brain.think("추가"))  # 이제 "insert"를 선택할 확률 높아짐
    print(brain.candidates["추가"])  # 가중치가 변경됨
