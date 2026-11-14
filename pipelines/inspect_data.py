"""실제 데이터 로드 전에 파일/컬럼 확인. python -m pipelines.inspect_data"""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

for filename in ("clean_reviews.csv", "filter_statistics.csv"):
    path = DATA_DIR / filename
    if not path.exists():
        print(f"[없음] {path} — data 안내문 참고")
        continue
    df = pd.read_csv(path, nrows=5)
    print(f"
[{filename}] columns={list(df.columns)}")
    print(df.head(3).to_string(index=False, max_colwidth=50))

meta = DATA_DIR / "products_meta.jsonl"
if meta.exists():
    sample = pd.read_json(meta, lines=True, nrows=3)
    print(f"
[products_meta.jsonl] columns={list(sample.columns)}")
else:
    print("
[선택] products_meta.jsonl 없음")
