"""최소 정규화 사전 예시. 실제 운영 전 검증된 용어 체계로 확장 필요."""
ASPECT_SYNONYMS = {
    "moisturizing": "hydration", "hydrating": "hydration",
    "scent": "fragrance", "fragrance": "fragrance",
    "sticky": "stickiness", "tacky": "stickiness",
}
SKIN_TYPES = {"dry skin": "dry", "oily skin": "oily", "combination skin": "combination"}

def normalize_aspect(term: str) -> str | None:
    return ASPECT_SYNONYMS.get(term.strip().lower())

def normalize_skin_type(term: str) -> str | None:
    return SKIN_TYPES.get(term.strip().lower())
