"""리뷰 원문 → Sentence Transformer 임베딩. DB 저장은 다음 단계."""
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def encode_reviews(texts: list[str]):
    model_name = os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL)
    model = SentenceTransformer(model_name)
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    if vectors.shape[1] != 384:
        raise ValueError("DB VECTOR(384)와 임베딩 차원이 다릅니다. schema.sql을 수정하세요.")
    return vectors
