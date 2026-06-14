class Brain:
    def __init__(self):
        self.candidates = {
            "추가": [("add", 0.9), ("insert", 0.1)],
            "수정": [("fix", 0.8), ("modify", 0.2)],
            "삭제": [("remove", 0.7), ("delete", 0.3)],
            "버그": [("bug", 1.0)],
            "로그인": [("login", 1.0)],
            "회원가입": [("signup", 0.9), ("register", 0.1)],
        }
        self.learning_rate = 0.1

    def think(self, sentence: str) -> str:
        words = sentence.strip().split()
        result_parts = []
        # [02와 차이] learn()을 위해 마지막 선택 기억
        self.last_selected = []

        for w in words:
            if w in self.candidates:
                best = max(self.candidates[w], key=lambda pair: pair[1])
                result_parts.append(best[0])
                self.last_selected.append((w, best))
            else:
                result_parts.append(w)
                self.last_selected.append((w, None))

        return ' '.join(result_parts)

    # [핵심 추가] 정답을 받아 가중치를 수동으로 올리고 내림
    def learn(self, correct_sentence: str):
        correct_words = correct_sentence.strip().split()

        for i, (word, selected) in enumerate(self.last_selected):
            if i >= len(correct_words) or selected is None or word not in self.candidates:
                continue

            correct = correct_words[i]
            if selected[0] != correct:
                self._decrease_weight(word, selected[0])
                self._increase_weight(word, correct)

    def _decrease_weight(self, word, wrong):
        for i, (trans, w) in enumerate(self.candidates[word]):
            if trans == wrong:
                self.candidates[word][i] = (trans, max(0.01, w - self.learning_rate))
                break

    def _increase_weight(self, word, correct):
        for i, (trans, w) in enumerate(self.candidates[word]):
            if trans == correct:
                self.candidates[word][i] = (trans, min(0.99, w + self.learning_rate))
                return
        # 후보에 없으면 새로 추가
        self.candidates[word].append((correct, 0.5))


if __name__ == "__main__":
    brain = Brain()

    print("=== 학습 전 ===")
    print(brain.think("추가"))
    print(brain.candidates["추가"])

    brain.think("추가")
    print("\n=== 학습: '추가' → 'insert' ===")
    brain.learn("insert")

    print("\n=== 학습 후 ===")
    print(brain.think("추가"))
    print(brain.candidates["추가"])
