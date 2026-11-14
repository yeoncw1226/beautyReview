import json
from rag.context_builder import build_context

def test_hybrid_filters_wrong_product_and_duplicate():
    result = json.loads(build_context(
        {"question":"보습력 어때?", "product_id":"A", "route":"hybrid"},
        {"product_id":"A", "count":10},
        [
            {"review_id":"1","product_id":"A","text":"좋음","similarity":0.9},
            {"review_id":"1","product_id":"A","text":"좋음","similarity":0.8},
            {"review_id":"2","product_id":"B","text":"다른 제품","similarity":0.99},
        ]
    ))
    assert result["statistics"]["count"] == 10
    assert [x["review_id"] for x in result["evidence"]] == ["1"]
