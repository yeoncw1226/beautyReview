"""관계 추출/검증 TODO.
GLiNER만으로 '누가 어떤 증상을 경험했는지'를 확정하면 안 됩니다.
"""

def parse_experiences(text: str, entities: list[dict]) -> list[dict]:
    raise NotImplementedError("관계 검증 및 occurred/improved/negated/unknown 분류 구현 필요")
