CONFIG_VERSION = "1.0"

COMMON_GLINER_LABELS = [
    "product material",
    "product defect",
    "product scent",
    "physical discomfort"
]

COMMON_ASPECTS = [
    "scent", "texture", "application",
    "effectiveness", "durability", "quality",
    "price", "packaging", "delivery", "appearance"
]

CATEGORY_CONFIG = {
    "skincare": {
        "gliner_labels": [
            "skin type", "skin condition",
            "cosmetic ingredient", "skin reaction",
            "skin hydration"
        ],
        "aspects": [
            "hydration", "absorption", "irritation",
            "acne", "brightening", "oil_control"
        ]
    },
    "haircare": {
        "gliner_labels": [
            "hair type", "hair condition",
            "scalp reaction", "hair product ingredient",
            "hair appearance"
        ],
        "aspects": [
            "frizz_control", "softness", "shine",
            "detangling", "scalp_comfort"
        ]
    },
    "makeup": {
        "gliner_labels": [
            "makeup shade", "skin type",
            "skin reaction", "makeup finish"
        ],
        "aspects": [
            "pigmentation", "color_match",
            "finish", "wear_time", "smudging"
        ]
    },
    "nailcare": {
        "gliner_labels": [
            "nail condition", "nail color",
            "nail reaction", "nail finish"
        ],
        "aspects": [
            "pigmentation", "drying_time",
            "durability", "finish", "removability"
        ]
    },
    "fragrance": {
        "gliner_labels": [
            "fragrance note", "scent intensity",
            "skin reaction"
        ],
        "aspects": [
            "scent", "longevity", "projection",
            "irritation"
        ]
    },
    "beauty_tools": {
        "gliner_labels": [
            "product material", "product defect",
            "physical discomfort"
        ],
        "aspects": [
            "usability", "durability",
            "effectiveness", "quality"
        ]
    },
    "hair_accessories": {
        "gliner_labels": [
            "hair type", "product material",
            "product defect"
        ],
        "aspects": [
            "comfort", "appearance",
            "shedding", "tangling", "durability"
        ]
    },
    "bath_body": {
        "gliner_labels": [
            "skin type", "cosmetic ingredient",
            "skin reaction"
        ],
        "aspects": [
            "hydration", "cleansing", "scent",
            "texture", "irritation"
        ]
    },
    "grooming": {
        "gliner_labels": [
            "facial hair type", "skin reaction",
            "grooming ingredient"
        ],
        "aspects": [
            "shaving_performance", "irritation",
            "smoothness", "durability"
        ]
    },
    "oralcare": {
        "gliner_labels": [
            "oral condition", "oral care ingredient",
            "oral reaction"
        ],
        "aspects": [
            "cleaning", "whitening",
            "sensitivity", "taste"
        ]
    },
    "other": {
        "gliner_labels": [
            "product feature", "product material",
            "product defect", "physical discomfort"
        ],
        "aspects": [
            "effectiveness", "quality",
            "durability", "usability"
        ]
    }
}

def get_category_config(category):
    return CATEGORY_CONFIG.get(
        category, CATEGORY_CONFIG["other"]
    )

def get_gliner_labels(category):
    config = get_category_config(category)
    return list(dict.fromkeys(
        COMMON_GLINER_LABELS + config["gliner_labels"]
    ))

def get_allowed_aspects(category):
    config = get_category_config(category)
    return list(dict.fromkeys(
        COMMON_ASPECTS + config["aspects"]
    ))
