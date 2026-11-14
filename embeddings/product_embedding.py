"""제품 프로필 텍스트 → 임베딩. 프로필 버전 변화시 재생성 필요."""
from embeddings.review_embedding import encode_reviews

def encode_product_profiles(profile_texts: list[str]):
    return encode_reviews(profile_texts)
