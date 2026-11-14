"""실제 CSV 스키마 확인 후 컬럼 매핑/배치 적재를 구현할 파일."""

def main():
    raise NotImplementedError(
        "먼저 python -m pipelines.inspect_data 로 CSV 컬럼과 timestamp 형식을 확인한 뒤 "
        "products → reviews → filter_statistics 순서의 배치 적재를 구현하세요."
    )

if __name__ == "__main__":
    main()
