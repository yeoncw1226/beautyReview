
from pathlib import Path
import argparse
import sys

import pandas as pd

# 프로젝트 루트를 import 경로에 추가
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from encoders.gliner_encoder import CosmeticGLiNER


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default="data/processed/reviews_sample_200.csv"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.3
    )
    parser.add_argument(
        "--model",
        default="urchade/gliner_small-v2.1"
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.is_absolute():
        input_path = ROOT / input_path

    if not input_path.exists():
        raise FileNotFoundError(input_path)

    df = pd.read_csv(
        input_path,
        dtype={"review_id": "string", "asin": "string"}
    )

    print("입력 리뷰 수:", len(df))
    print("\n카테고리 분포:")
    print(df["product_category"].value_counts())

    model = CosmeticGLiNER(
        model_name=args.model,
        threshold=args.threshold,
        batch_size=args.batch_size
    )

    entity_df, status_df = model.encode_dataframe(df)

    output_dir = ROOT / "data" / "encoded"
    output_dir.mkdir(parents=True, exist_ok=True)

    entity_df.to_parquet(
        output_dir / "gliner_entities.parquet",
        index=False
    )

    status_df.to_parquet(
        output_dir / "gliner_status.parquet",
        index=False
    )

    # 원문 리뷰를 붙인 검토용 CSV
    result_view = entity_df.merge(
        df[["review_id", "text"]],
        on="review_id",
        how="left",
        validate="many_to_one"
    )

    result_view.to_csv(
        output_dir / "gliner_results_sample.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== 라벨별 빈도 =====")
    print(entity_df["entity_label"].value_counts())

    print("\n===== 추출 예시 =====")
    print(
        result_view[
            ["product_category", "entity_text",
             "entity_label", "score"]
        ].head(20).to_string(index=False)
    )

    print("\n결과 저장 위치:", output_dir)


if __name__ == "__main__":
    main()
