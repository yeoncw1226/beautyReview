# 개발 체크리스트

- [ ] `.env` 설정, PostgreSQL 및 pgvector 준비
- [ ] `schema.sql` 실행, 12개 테이블 확인
- [ ] 실제 CSV 컬럼/결측/중복/타임스탬프 단위 점검
- [ ] `load_raw_data.py` 배치 적재 구현 (첫 100~300개 리뷰)
- [ ] PyABSA 사전학습 모델 출력과 화장품 속성 정답셋 대조
- [ ] GLiNER 라벨/임계값 평가, 관계 검증
- [ ] ASIN별 속성·경험 통계와 분모 정의
- [ ] review-only product profile 생성
- [ ] Sentence Transformer 임베딩 및 차원 검증
- [ ] pgvector 검색 / SQL 집계 검증
- [ ] LangChain 질문 라우팅 / 검색 / Context / LLM 통합
- [ ] 제품 후보 검색 + SQL 재정렬 + 근거 설명 구현

**기술 주의:** PyABSA 설치가 Python 3.13+에서 충돌할 수 있어 별도 Python 3.10 환경을 권장합니다. Colab에서 생성한 분석 결과를 JSONL로 내보내 Windows PostgreSQL에 적재하는 구성도 가능합니다.
