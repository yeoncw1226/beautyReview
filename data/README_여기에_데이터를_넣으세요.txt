이 폴더에는 실제 데이터 파일이 포함되어 있지 않습니다.

여기에 둘 파일:
1. clean_reviews.csv
   - Colab 필터링을 통과한 리뷰
   - 기대 컬럼 예: asin, parent_asin, text, rating, title, user_id, timestamp, verified_purchase, helpful_vote, images
   - 실제 컬럼은 반드시 먼저 확인하세요. review_id가 없으면 안정적인 ID 생성 방식이 필요합니다.
2. filter_statistics.csv
   - asin별 필터링 전후 개수 및 AI-generated/Paid 의심 제외 통계
   - 컬럼 이름, 단위, 순차 필터링 순서를 확인하세요.
3. products_meta.jsonl (선택)
   - Amazon 2023 제품 메타 데이터
   - asin 또는 parent_asin 연결 방식 확인 필요. 없는 description은 NULL로 둡니다.

Colab 분석 결과를 따로 저장할 경우:
4. absa_results.jsonl (선택)
5. gliner_results.jsonl (선택)

현재 데이터는 없으므로 load_raw_data.py는 데이터 스키마가 확인될 때까지 구현하지 않았습니다.
+인코딩 결과
