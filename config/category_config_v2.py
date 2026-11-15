CONFIG_VERSION = "2.0"

# ==============================================================================
# 1. COMMON GLINER LABELS (Entity Extraction Prompts)
# - Designed as clean, natural language noun phrases for optimal zero-shot recall.
# - Pure opinion/sentiment clusters (e.g., "horrible", "does not work") are excluded
#   so PyABSA can accurately resolve polarity on concrete aspects.
# ==============================================================================
COMMON_GLINER_LABELS = [
    "cosmetic ingredient",      # Cluster 2, 8, 25 (silicone, oils, active ingredients)
    "product scent",            # Cluster 13, 36 (fragrance, odor, chemical smell)
    "texture or feel",          # Cluster 6, 18, 27 (smooth, sticky, greasy, drying)
    "packaging or container",   # Cluster 29, 39, 12 (bottle, pump, wrapper, sprayer)
    "physical defect",          # Cluster 16, 37 (broken, cracked, damaged, leaking)
    "adverse reaction"          # Cluster 7, 30 (pain, burning, itchy skin, rash)
]

# ==============================================================================
# 2. COMMON ASPECTS (PyABSA Target Aspect Schema)
# ==============================================================================
COMMON_ASPECTS = [
    "scent", "texture", "application",
    "effectiveness", "durability", "quality",
    "price", "packaging", "delivery", "appearance",
    "irritation", "defect"
]

# ==============================================================================
# 3. CATEGORY-SPECIFIC CONFIGURATIONS
# ==============================================================================
CATEGORY_CONFIG = {
    "skincare": {
        "gliner_labels": [
            "skin type or condition",   # Cluster 4 (sensitive skin, acne, oily skin)
            "facial area or mask",      # Cluster 19 (forehead, lips, face mask)
            "eye area product"          # Cluster 9 (eye cream, dry eye)
        ],
        "aspects": [
            "hydration", "absorption", "irritation",
            "acne", "brightening", "oil_control", "soothing"
        ]
    },
    "haircare": {
        "gliner_labels": [
            "hair type or style",       # Cluster 21 (curly hair, thick hair, fine hair)
            "hair product or scalp",    # Cluster 20 (shampoo, conditioner, scalp, dandruff)
            "color or shade"            # Cluster 23, 0, 22 (hair color, tint, shine)
        ],
        "aspects": [
            "frizz_control", "softness", "shine",
            "detangling", "scalp_comfort", "hydration", "color_retention"
        ]
    },
    "makeup": {
        "gliner_labels": [
            "color or makeup shade",    # Cluster 23, 0, 22 (dark brown, shimmer, tint)
            "eye or lash makeup",       # Cluster 9 (eyelashes, mascara, eyeliner)
            "skin type or condition",   # Cluster 4 (oily skin, sensitive skin)
            "product flavor"            # Cluster 35 (lip product flavor/taste)
        ],
        "aspects": [
            "pigmentation", "color_match",
            "finish", "wear_time", "smudging", "blendability"
        ]
    },
    "nailcare": {
        "gliner_labels": [
            "nail product or finish",   # Cluster 5, 31 (gel polish, top coat, matte polish)
            "color or shade",           # Cluster 23, 0 (nail color, glitter, shine)
            "adhesive or glue"          # Cluster 18 (nail glue, adhesion)
        ],
        "aspects": [
            "pigmentation", "drying_time",
            "durability", "finish", "removability", "adhesion"
        ]
    },
    "fragrance": {
        "gliner_labels": [
            "fragrance note",           # Cluster 13, 35, 38 (lavender, vanilla, sandalwood)
            "scent intensity"           # Cluster 13, 36 (light scent, strong odor)
        ],
        "aspects": [
            "scent", "longevity", "projection",
            "irritation"
        ]
    },
    "beauty_tools": {
        "gliner_labels": [
            "beauty tool or device",    # Cluster 14, 15 (brushes, applicators, shaver)
            "product material",         # Cluster 28, 3 (fabric, metal, bristles)
            "size or fit"               # Cluster 17 (size, tight, elastic)
        ],
        "aspects": [
            "usability", "durability",
            "effectiveness", "quality", "comfort"
        ]
    },
    "hair_accessories": {
        "gliner_labels": [
            "hair type or style",       # Cluster 21 (wig hair, human hair, curly hair)
            "product material",         # Cluster 28, 3 (fabric, cotton, silk, metal)
            "size or fit",              # Cluster 17 (elastic, tight, stretch, lace front)
            "color or shade"            # Cluster 23, 22 (hair color, wave, tint)
        ],
        "aspects": [
            "comfort", "appearance",
            "shedding", "tangling", "durability", "fit"
        ]
    },
    "bath_body": {
        "gliner_labels": [
            "skin type or condition",   # Cluster 4 (dry skin, sensitive skin, eczema)
            "product flavor"            # Cluster 35 (coconut, berry, vanilla)
        ],
        "aspects": [
            "hydration", "cleansing", "scent",
            "texture", "irritation", "lather"
        ]
    },
    "grooming": {
        "gliner_labels": [
            "facial hair or shaving tool", # Cluster 15 (beard, mustache, razor blades, shaver)
            "skin type or condition"       # Cluster 4 (sensitive skin, razor bumps)
        ],
        "aspects": [
            "shaving_performance", "irritation",
            "smoothness", "durability", "precision"
        ]
    },
    "oralcare": {
        "gliner_labels": [
            "oral care tool or condition", # Cluster 14 (toothbrush, bristles, plaque, gums)
            "product flavor"               # Cluster 35 (mint flavor, peppermint)
        ],
        "aspects": [
            "cleaning", "whitening",
            "sensitivity", "taste", "freshness"
        ]
    },
    "other": {
        "gliner_labels": [
            "product material",         # Cluster 28, 3
            "size or fit",              # Cluster 17
            "product flavor"            # Cluster 35
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
