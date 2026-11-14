
import hashlib
import time

import pandas as pd
import torch

from gliner import GLiNER
from tqdm.auto import tqdm

from config.category_config import (
    CONFIG_VERSION,
    get_gliner_labels
)


ENTITY_COLUMNS = [
    "review_id",
    "entity_id",
    "asin",
    "product_category",
    "entity_text",
    "entity_label",
    "raw_label",
    "start",
    "end",
    "score",
    "context",
    "model_version",
    "label_config_version"
]

STATUS_COLUMNS = [
    "review_id",
    "asin",
    "product_category",
    "analysis_status",
    "entity_count",
    "error_message",
    "model_version",
    "label_config_version"
]


def normalize_label(label):
    """GLiNER 입력 라벨을 snake_case로 변환"""
    mapping = {
        "cosmetic ingredient": "ingredient",
        "hair product ingredient": "ingredient",
        "grooming ingredient": "ingredient",
        "oral care ingredient": "ingredient",
        "product material": "material",
        "makeup shade": "shade",
        "nail color": "shade",
        "makeup finish": "finish",
        "nail finish": "finish",
    }

    return mapping.get(
        label, label.lower().replace(" ", "_")
    )


class CosmeticGLiNER:

    def __init__(
        self,
        model_name="urchade/gliner_small-v2.1",
        threshold=0.3,
        batch_size=16,
        device=None
    ):
        self.model_name = model_name
        self.threshold = threshold
        self.batch_size = batch_size

        self.device = device or (
            "cuda" if torch.cuda.is_available()
            else "cpu"
        )

        print(f"GLiNER 모델 로딩: {model_name}")
        print(f"사용 장치: {self.device}")

        self.model = GLiNER.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        print("모델 로딩 완료")

    def make_entity_id(
        self, review_id, start, end, label
    ):
        key = (
            f"{review_id}|{start}|{end}|{label}|"
            f"{self.model_name}|{CONFIG_VERSION}"
        )

        return hashlib.sha256(
            key.encode("utf-8")
        ).hexdigest()[:20]

    def predict_batch(self, texts, category):

        labels = get_gliner_labels(category)

        with torch.inference_mode():
            return self.model.inference(
                texts,
                labels,
                batch_size=self.batch_size,
                threshold=self.threshold
            )

    def encode_dataframe(self, df):

        required = [
            "review_id", "asin",
            "product_category", "text"
        ]

        missing = [
            col for col in required
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"필수 컬럼 누락: {missing}"
            )

        if df["review_id"].isna().any():
            raise ValueError("review_id 결측값 존재")

        if not df["review_id"].is_unique:
            raise ValueError("review_id 중복 존재")

        work = df[required].copy()

        work["text"] = (
            work["text"].fillna("").astype(str)
        )

        work["product_category"] = (
            work["product_category"]
            .fillna("other")
            .astype(str)
        )

        entities_output = []
        status_output = []

        start_time = time.perf_counter()

        # 카테고리별 분석
        for category, group in work.groupby(
            "product_category", sort=False
        ):

            group = group.reset_index(drop=True)

            for start in tqdm(
                range(0, len(group), self.batch_size),
                desc=f"GLiNER: {category}"
            ):

                batch = group.iloc[
                    start:start + self.batch_size
                ]

                texts = batch["text"].tolist()

                try:
                    predictions = self.predict_batch(
                        texts, category
                    )

                    if len(predictions) != len(batch):
                        raise RuntimeError(
                            "배치 결과 개수 불일치"
                        )

                except Exception as exc:
                    for _, row in batch.iterrows():
                        status_output.append({
                            "review_id": row["review_id"],
                            "asin": row["asin"],
                            "product_category": category,
                            "analysis_status": "error",
                            "entity_count": 0,
                            "error_message": str(exc)[:500],
                            "model_version": self.model_name,
                            "label_config_version": CONFIG_VERSION
                        })
                    continue

                for (_, row), result in zip(
                    batch.iterrows(), predictions
                ):

                    text = row["text"]
                    review_id = row["review_id"]
                    count = 0

                    for ent in result:

                        s = int(ent["start"])
                        e = int(ent["end"])

                        if not (0 <= s < e <= len(text)):
                            continue

                        raw_label = ent["label"]

                        entity_id = self.make_entity_id(
                            review_id, s, e, raw_label
                        )

                        entities_output.append({
                            "review_id": review_id,
                            "entity_id": entity_id,
                            "asin": row["asin"],
                            "product_category": category,
                            "entity_text": text[s:e],
                            "entity_label": normalize_label(
                                raw_label
                            ),
                            "raw_label": raw_label,
                            "start": s,
                            "end": e,
                            "score": float(ent["score"]),
                            "context": text[
                                max(0, s - 60):
                                min(len(text), e + 60)
                            ],
                            "model_version": self.model_name,
                            "label_config_version": CONFIG_VERSION
                        })

                        count += 1

                    status_output.append({
                        "review_id": review_id,
                        "asin": row["asin"],
                        "product_category": category,
                        "analysis_status": (
                            "success" if count > 0
                            else "no_entities"
                        ),
                        "entity_count": count,
                        "error_message": None,
                        "model_version": self.model_name,
                        "label_config_version": CONFIG_VERSION
                    })

        elapsed = time.perf_counter() - start_time

        entity_df = pd.DataFrame(
            entities_output,
            columns=ENTITY_COLUMNS
        )

        status_df = pd.DataFrame(
            status_output,
            columns=STATUS_COLUMNS
        )

        print("\n===== GLiNER 분석 결과 =====")
        print(f"전체 리뷰: {len(work):,}")
        print(f"추출 엔티티: {len(entity_df):,}")
        print(f"실행 시간: {elapsed/60:.2f}분")
        print(
            f"처리 속도: "
            f"{len(work)/max(elapsed, 1e-9):.2f} reviews/sec"
        )

        print("\n분석 상태:")
        print(status_df["analysis_status"].value_counts())

        return entity_df, status_df