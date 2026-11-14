"""SQL 통계 / pgvector 검색 모듈 구현 위치. 미구현."""

def search_sql(plan):
    raise NotImplementedError("정적 매개변수 SQL 또는 검증된 쿼리 빌더로 구현")

def search_vector(plan):
    raise NotImplementedError("동일 임베딩 모델로 질문 벡터를 만들고 product_id 필터")
