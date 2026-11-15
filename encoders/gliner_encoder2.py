"""GLiNER entity extraction with APC routing and pre-marked APC inputs.

Existing fields: review_id, text, label, start, end, score.
Additional fields: entity_role, apc_eligible, apc_input, and traceability metadata.
No PyABSA inference or normalization is performed in this module.
"""
from __future__ import annotations

from typing import Any, Iterable
from category_config_v3 import get_gliner_labels, route_entity_label


def mark_apc_input(review_text: str, start: int, end: int) -> str:
    """Insert PyABSA aspect markers using GLiNER's ORIGINAL character offsets."""
    if not isinstance(review_text, str):
        raise TypeError("review_text must be str")
    if not isinstance(start, int) or not isinstance(end, int) or isinstance(start, bool) or isinstance(end, bool):
        raise ValueError("start/end must be integer character offsets")
    if not (0 <= start < end <= len(review_text)):
        raise ValueError("Invalid GLiNER span")
    return (review_text[:start] + "[B-ASP]" + review_text[start:end]
            + "[E-ASP]" + review_text[end:])


def prepare_entities(review_id: Any, review_text: str, category: str,
                     predictions: Iterable[dict]) -> list[dict[str, Any]]:
    """Convert GLiNER predictions to routable records without silently fixing bad spans."""
    if not isinstance(review_text, str) or not review_text.strip():
        return []
    records = []
    for pred in predictions:
        start, end = pred.get("start"), pred.get("end")
        valid_span = (isinstance(start, int) and not isinstance(start, bool)
                      and isinstance(end, int) and not isinstance(end, bool)
                      and 0 <= start < end <= len(review_text))
        extracted = str(pred.get("text", ""))
        span_matches = valid_span and review_text[start:end] == extracted
        route = route_entity_label(pred.get("label", ""))
        # Don't send bad spans or inconsistent GLiNER outputs to APC.
        can_apc = bool(route["apc_eligible"] and span_matches)
        record = {
            "review_id": str(review_id),
            "review_text": review_text,
            "product_category": category,
            "text": extracted,
            "label": pred.get("label"),
            "start": start,
            "end": end,
            "score": pred.get("score"),
            "entity_role": route["entity_role"],
            "apc_eligible": can_apc,
            "apc_input": mark_apc_input(review_text, start, end) if can_apc else None,
            "span_valid": bool(span_matches),
            "routing_reason": ("invalid_or_mismatched_span" if not span_matches
                               else "label_route:" + route["entity_role"]),
        }
        records.append(record)
    return records


class GLiNEREncoder:
    """Usage: GLiNEREncoder().encode(review_id, text, category='skincare')."""

    def __init__(self, model_name: str = "urchade/gliner_medium-v2.1",
                 threshold: float = 0.5, device: str | None = None):
        from gliner import GLiNER
        self.model = GLiNER.from_pretrained(model_name)
        if device is not None:
            self.model = self.model.to(device)
        self.threshold = threshold

    def encode(self, review_id: Any, text: str, category: str = "other") -> list[dict[str, Any]]:
        if not isinstance(text, str) or not text.strip():
            return []
        labels = get_gliner_labels(category)
        predictions = self.model.predict_entities(text, labels, threshold=self.threshold)
        return prepare_entities(review_id, text, category, predictions)


if __name__ == "__main__":
    review = "The fragrance is amazing, but the texture is sticky."
    entities = [
        {"text": "fragrance", "label": "product scent", "start": 4, "end": 13, "score": 0.98},
        {"text": "texture", "label": "texture or feel", "start": 34, "end": 41, "score": 0.94},
    ]
    for row in prepare_entities("R001", review, "skincare", entities):
        print({k: row[k] for k in ("text", "label", "apc_eligible", "apc_input")})
