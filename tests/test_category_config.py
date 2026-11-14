from config.category_config import (
    CATEGORY_CONFIG,
    get_gliner_labels,
    get_allowed_aspects
)

def test_categories():
    assert len(CATEGORY_CONFIG) == 11

def test_skincare():
    assert "skin type" in get_gliner_labels("skincare")
    assert "hydration" in get_allowed_aspects("skincare")

def test_unknown_category():
    assert get_gliner_labels("unknown") == get_gliner_labels("other")
