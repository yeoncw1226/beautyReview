"""조회 결과를 LLM용 구조화 Context로 정리하는 최소 예시.
통계 결과는 검색된 Top-K 리뷰로 계산하지 말고 SQL에서 따로 가져오세요.
"""
import json

def build_context(plan: dict, sql_result: dict | None = None,
                  vector_results: list[dict] | None = None, max_reviews: int = 5) -> str:
    product_id = plan.get("product_id")
    route = plan.get("route")
    if route not in ("sql", "vector", "hybrid"):
        raise ValueError("route must be sql, vector, or hybrid")
    out = {"question": plan.get("question"), "product_id": product_id,
           "statistics": None, "evidence": [], "limitations": []}
    if route in ("sql", "hybrid"):
        if sql_result and sql_result.get("product_id") == product_id:
            out["statistics"] = sql_result
        else:
            out["limitations"].append("SQL statistics unavailable or mismatched")
    if route in ("vector", "hybrid"):
        seen = set()
        rows = sorted(vector_results or [], key=lambda x: x.get("similarity", 0), reverse=True)
        for item in rows:
            rid = item.get("review_id")
            if item.get("product_id") != product_id or not rid or rid in seen:
                continue
            seen.add(rid)
            out["evidence"].append({"review_id": rid, "text": item.get("text", "")})
            if len(out["evidence"]) >= max_reviews:
                break
        if not out["evidence"]:
            out["limitations"].append("Relevant evidence unavailable")
    return json.dumps(out, ensure_ascii=False, indent=2)
