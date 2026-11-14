# Cosmetics Review RAG — VS Code Starter

Amazon 화장품 리뷰 중심 PostgreSQL + pgvector + LangChain 프로젝트의 **시작용 골격**입니다.
데이터 및 API 키는 포함하지 않았습니다. 완성된 서비스가 아닌, 데이터 적재·분석·검색 모듈을 단계별로 채워 넣기 위한 구조입니다.

## 빠른 시작 (Windows PowerShell / VS Code)

1. 폴더를 VS Code에서 열고 `Python: Select Interpreter`로 프로젝트 가상환경을 지정하세요.
2. Python 3.10 또는 3.11 환경 권장 (PyABSA는 별도 호환 환경을 권장). GPU/Colab에서 분석하고 결과만 DB에 적재해도 됩니다.
3. 가상환경과 기본 라이브러리 설치:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
4. `.env.example`을 `.env`로 복사하고 PostgreSQL 접속 주소를 입력하세요.
5. PostgreSQL 서버를 준비하고 `CREATE EXTENSION vector` 권한을 확인하세요. `database/schema.sql`을 DB에서 실행하세요.
6. `data/README_여기에_데이터를_넣으세요.txt`에 맞춰 CSV/JSONL을 배치하세요.
7. `python -m pipelines.inspect_data`로 컬럼을 먼저 검사하세요.
8. `python -m pipelines.load_raw_data`는 **미구현 스텁**입니다. 실제 CSV 컬럼이 확인된 뒤 매핑을 작성하세요.

## 권장 개발 순서

`database/schema.sql` → CSV 컬럼 검증 → 원본 적재 → PyABSA/GLiNER 소규모 평가 → 정규화 및 경험 관계 검증 → 제품 통계/프로필 → 리뷰·제품 임베딩 → SQL/Vector Retriever → Context Builder → RAG.

## 폴더 안내

- `data/`: 사용자 제공 데이터만 저장 (Git 제외). 실제 데이터는 없음
- `database/`: 12개 기본 테이블 SQL 및 연결
- `encoders/`: PyABSA, GLiNER, 관계 검증, 정규화 모듈의 **구현 템플릿**
- `embeddings/`: Sentence Transformer 임베딩과 적재용 **템플릿**
- `pipelines/`: CSV 점검, 원본 적재, 인코딩, 제품 프로필 생성용 **템플릿**
- `rag/`: 질문 라우팅, 검색, Context 생성, 답변 생성용 **템플릿**
- `docs/`: 스키마/구현 순서 참고
- `tests/`: 기본 Context Builder 검증

## 중요 원칙

- 제품 정보 누락은 `NULL`로 유지하며 리뷰 기반 분석을 우선합니다.
- 추출된 피부 타입과 경험의 관계는 검증 전 확정하지 않습니다.
- 통계는 전체 적격 리뷰 기반으로 계산하며, 벡터 Top-K 결과로 통계 비율을 계산하지 않습니다.
- AI/Paid 필터링 결과는 모델의 **의심·제외 수치**이지 확정 가짜 리뷰 비율이 아닙니다.
- 리뷰 및 제품 임베딩은 사용한 모델 이름과 차원을 기록해야 합니다.
- API 키와 실제 데이터는 커밋하지 마세요.
