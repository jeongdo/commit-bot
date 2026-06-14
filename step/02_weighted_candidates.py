class Brain:
    def __init__(self):
        # [01과 차이] 고정 매핑 → (번역어, 가중치) 후보 목록으로 변경
        self.candidates = {
            "추가":    [("add", 0.9), ("insert", 0.1)],
            "수정":    [("fix", 0.8), ("modify", 0.2)],
            "삭제":    [("remove", 0.7), ("delete", 0.3)],
            "버그":    [("bug", 1.0)],
            "로그인":  [("login", 1.0)],
            "회원가입": [("signup", 0.9), ("register", 0.1)],
        }
        self.weights = [0.5] * 10  # Step-03 학습용 더미

    def think(self, sentence: str) -> str:
        words = sentence.strip().split()
        result_parts = []

        for w in words:
            if w in self.candidates:
                # [핵심] 가중치가 가장 높은 후보 선택
                best = max(self.candidates[w], key=lambda pair: pair[1])
                result_parts.append(best[0])
            else:
                result_parts.append(w)

        return ' '.join(result_parts)


if __name__ == "__main__":
    brain = Brain()
    test_cases = ["로그인 추가", "버그 수정", "회원가입 삭제", "모르는단어 추가"]
    for case in test_cases:
        print(f"{case:10} → {brain.think(case)}")
