
import json
from pathlib import Path

from config.category_config import get_gliner_labels

EXPERIMENT_DIR = Path(__file__).parent / "experiments"


def load_experiment(version="v1"):
    path = EXPERIMENT_DIR / f"gliner_{version}.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_experiment_labels(category, experiment):
    original_labels = get_gliner_labels(category)

    overrides = experiment.get("label_overrides", {})

    return [
        overrides.get(label, label)
        for label in original_labels
    ]
