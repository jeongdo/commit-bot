class Brain:
    def __init__(self):
        # 각 한글 단어 → (영어 후보, 가중치) 리스트
        # 가중치가 높을수록 우선 선택됨
        self.candidates = {
            "추가":   [("add", 0.9), ("insert", 0.1)], # "추가"라는 한글을 보면 → "add"를 90% 선호, "insert"를 10% 선호
            "수정":   [("fix", 0.8), ("modify", 0.2)],
            "삭제":   [("remove", 0.7), ("delete", 0.3)],
            "버그":   [("bug", 1.0)],
            "로그인": [("login", 1.0)],
            "회원가입": [("signup", 0.9), ("register", 0.1)],
        }
        # (참고) Step-03에서 학습할 때 쓸 가중치 저장소
        self.weights = [0.5] * 10   # 일단 더미로 보관

    def think(self, sentence: str) -> str:
        """
        한국어 문장을 입력받아 영어 커밋 메시지로 변환
        예: "로그인 추가" → "login add"
        """
        words = sentence.strip().split()
        result_parts = []

        for w in words:
            if w in self.candidates:
                # 가중치가 가장 높은 후보를 선택
                best_candidate = max(self.candidates[w], key=lambda pair: pair[1])
                result_parts.append(best_candidate[0])
            else:
                # 모르는 단어는 원형 그대로 보존
                result_parts.append(w)

        return ' '.join(result_parts)


# 테스트
if __name__ == "__main__":
    brain = Brain()
    test_cases = [
        "로그인 추가",
        "버그 수정",
        "회원가입 삭제",
        "모르는단어 추가"
    ]
    for case in test_cases:
        print(f"{case:10} → {brain.think(case)}")