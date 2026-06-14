# [03과 차이] 로직 동일, 실행부에서 역전 과정을 step별로 시각화한 데모

class Brain:
    def __init__(self):
        # 초기엔 remove 우세 → 학습으로 delete가 역전하는 과정을 확인
        self.candidates = {
            "삭제": [("remove", 0.7), ("delete", 0.3)],
        }
        self.learning_rate = 0.1
        self.last_selected = []

    def think(self, sentence: str) -> str:
        words = sentence.strip().split()
        result_parts = []
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
        self.candidates[word].append((correct, 0.5))

    def show_status(self, word):
        print(f"  {self.candidates[word]}")


if __name__ == "__main__":
    brain = Brain()
    print("📚 '삭제' 단어 학습 역전 과정 (remove → delete)")

    for step in range(8):
        print(f"\n[Step {step}] 현재 상태:", end="")
        brain.show_status("삭제")

        result = brain.think("삭제")
        print(f"  🤔 생각한 결과: '{result}'")

        if result == "remove":
            print(f"  📖 학습: '삭제'는 'delete'가 정답!")
            brain.learn("delete")
        else:
            print(f"  ✅ 목표 달성! 'delete'를 선택함")
            break

    print("\n🎯 최종 결과")
    brain.show_status("삭제")
