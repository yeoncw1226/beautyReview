"""GLiNER label configuration and conservative APC routing (v3.0).

Routes are based only on GLiNER labels; mixed labels remain in REVIEW_REQUIRED.
Do not interpret apc_eligible=True as evidence of an actual sentiment.
"""
CONFIG_VERSION = "3.0"

COMMON_GLINER_LABELS = [
    "cosmetic ingredient", "product scent", "texture or feel",
    "packaging or container", "physical defect", "adverse reaction",
]

CATEGORY_CONFIG = {
    "skincare": {"gliner_labels": ["skin type or condition", "facial area or mask", "eye area product"]},
    "haircare": {"gliner_labels": ["hair type or style", "hair product or scalp", "color or shade"]},
    "makeup": {"gliner_labels": ["color or makeup shade", "eye or lash makeup", "skin type or condition", "product flavor"]},
    "nailcare": {"gliner_labels": ["nail product or finish", "color or shade", "adhesive or glue"]},
    "fragrance": {"gliner_labels": ["fragrance note", "scent intensity"]},
    "beauty_tools": {"gliner_labels": ["beauty tool or device", "product material", "size or fit"]},
    "hair_accessories": {"gliner_labels": ["hair type or style", "product material", "size or fit", "color or shade"]},
    "bath_body": {"gliner_labels": ["skin type or condition", "product flavor"]},
    "grooming": {"gliner_labels": ["facial hair or shaving tool", "skin type or condition"]},
    "oralcare": {"gliner_labels": ["oral care tool or condition", "product flavor"]},
    "other": {"gliner_labels": ["product material", "size or fit", "product flavor"]},
}

# Only labels with reasonably consistent semantic roles are auto-routed.
# Mixed labels are REVIEW_REQUIRED rather than silently misrouted.
LABEL_ROUTES = {
    "product scent": "EVALUATION",
    "texture or feel": "EVALUATION",
    "packaging or container": "EVALUATION",
    "color or shade": "EVALUATION",
    "color or makeup shade": "EVALUATION",
    "product flavor": "EVALUATION",
    "fragrance note": "EVALUATION",
    "scent intensity": "EVALUATION",
    "product material": "EVALUATION",
    "size or fit": "EVALUATION",
    "beauty tool or device": "EVALUATION",
    "eye area product": "EVALUATION",
    "eye or lash makeup": "EVALUATION",
    "nail product or finish": "EVALUATION",
    "adhesive or glue": "EVALUATION",
    "cosmetic ingredient": "REVIEW_REQUIRED",  # May just be an ingredients list
    "skin type or condition": "REVIEW_REQUIRED",  # oily skin vs acne
    "facial area or mask": "REVIEW_REQUIRED",  # forehead vs mask
    "hair type or style": "CONTEXT",  # provisional; product hair styles can vary
    "hair product or scalp": "REVIEW_REQUIRED",
    "physical defect": "EXPERIENCE",
    "adverse reaction": "EXPERIENCE",
    "facial hair or shaving tool": "REVIEW_REQUIRED",
    "oral care tool or condition": "REVIEW_REQUIRED",
}

APC_ELIGIBLE_ROUTES = {"EVALUATION"}


def get_category_config(category):
    return CATEGORY_CONFIG.get(str(category).strip().lower(), CATEGORY_CONFIG["other"])


def get_gliner_labels(category):
    return list(dict.fromkeys(COMMON_GLINER_LABELS + get_category_config(category)["gliner_labels"]))


def route_entity_label(label):
    """Return role and APC eligibility. Unknown or mixed labels are held for review."""
    route = LABEL_ROUTES.get(str(label).strip().lower(), "REVIEW_REQUIRED")
    return {"entity_role": route, "apc_eligible": route in APC_ELIGIBLE_ROUTES}


def get_apc_eligible(label):
    return route_entity_label(label)["apc_eligible"]


def validate_routing():
    labels = set(COMMON_GLINER_LABELS)
    for config in CATEGORY_CONFIG.values():
        labels.update(config["gliner_labels"])
    return sorted(labels - LABEL_ROUTES.keys())


if __name__ == "__main__":
    print("Unmapped labels:", validate_routing())
