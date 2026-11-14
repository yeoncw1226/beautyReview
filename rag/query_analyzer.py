"""사용자 질문을 조건과 SQL/Vector/Hybrid 경로로 분류하는 LLM 구현 위치."""
from typing import Literal
from pydantic import BaseModel

class QueryPlan(BaseModel):
    question: str
    route: Literal["sql", "vector", "hybrid"]
    product_id: str | None = None
    skin_type: str | None = None
    aspects: list[str] = []


def analyze_question(question: str) -> QueryPlan:
    raise NotImplementedError("실제 LLM의 Structured Output으로 연결 필요")
