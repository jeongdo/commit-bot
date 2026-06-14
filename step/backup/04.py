# 04.py
class Brain:
    def __init__(self):
        self.candidates = {
            "삭제": [("remove", 0.7), ("delete", 0.3)],  # 초기엔 remove 우세
        }
        self.learning_rate = 0.1
        self.last_selected = []
        self.last_input_words = []

    def think(self, sentence: str) -> str:
        words = sentence.strip().split()
        result_parts = []
        self.last_input_words = words
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

        for i, (original_word, selected) in enumerate(self.last_selected):
            if i >= len(correct_words):
                break
            if selected is None or original_word not in self.candidates:
                continue

            correct_word = correct_words[i]
            if selected[0] != correct_word:
                self._decrease_weight(original_word, selected[0])
                self._increase_weight(original_word, correct_word)

    def _decrease_weight(self, word, wrong_translation):
        for i, (trans, weight) in enumerate(self.candidates[word]):
            if trans == wrong_translation:
                new_weight = weight - self.learning_rate
                self.candidates[word][i] = (trans, max(0.01, new_weight))
                break

    def _increase_weight(self, word, correct_translation):
        for i, (trans, weight) in enumerate(self.candidates[word]):
            if trans == correct_translation:
                new_weight = weight + self.learning_rate
                self.candidates[word][i] = (trans, min(0.99, new_weight))
                break
        else:
            self.candidates[word].append((correct_translation, 0.5))

    def show_status(self, word):
        """현재 가중치 상태 보여주기"""
        print(f"  {self.candidates[word]}")


# 실행 데모
if __name__ == "__main__":
    brain = Brain()

    print("=" * 50)
    print("📚 '삭제' 단어 학습 역전 과정")
    print("=" * 50)

    for step in range(8):
        print(f"\n[Step {step}] 현재 상태:", end="")
        brain.show_status("삭제")

        # 생각하고 결과 보여주기
        result = brain.think("삭제")
        print(f"  🤔 생각한 결과: '{result}'")

        if result == "remove":
            # remove를 골랐으면 "delete"가 정답이라고 학습
            print(f"  📖 학습: '삭제'는 'delete'가 정답이야!")
            brain.learn("delete")
        else:
            # delete를 골랐으면 학습 중단 (이미 목표 달성)
            print(f"  ✅ 목표 달성! 'delete'를 선택함")
            break

    print("\n" + "=" * 50)
    print("🎯 최종 결과")
    brain.show_status("삭제")
    print(f"🤔 최종 생각: '{brain.think('삭제')}'")