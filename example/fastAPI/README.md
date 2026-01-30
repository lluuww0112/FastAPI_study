# FastAPI 학습 예제

이 디렉토리는 FastAPI와 데이터베이스를 사용한 웹 API 개발을 순차적으로 학습하기 위한 예제 코드입니다.

```bash
example/
├── README.md                    # 전체 학습 가이드
├── step01_basic_fastapi/        # FastAPI 기본
├── step02_routers/              # 라우터 기본
├── step03_sqlmodel_basic/       # SQLModel 모델 정의
├── step04_database_connection/  # 데이터베이스 연결
├── step05_create/               # 데이터 생성 (POST)
├── step06_read/                 # 데이터 조회 (GET)
├── step07_update/               # 데이터 수정 (PUT)
├── step08_delete/               # 데이터 삭제 (DELETE)
├── step09_relationships/        # 테이블 간 관계
├── step10_error_handling/       # 에러 처리
└── step11_router_separation/    # 라우터 분리 및 구조화
```


## 학습 순서

각 단계는 독립적으로 실행 가능하며, 순서대로 학습하는 것을 권장합니다.

### Step 1: FastAPI 기본
- FastAPI 애플리케이션 생성
- 기본 라우트 정의
- 실행 방법

### Step 2: 라우터 기본
- APIRouter 사용법
- 라우터 등록
- 태그 및 설명 추가

### Step 3: SQLModel 기본 모델 정의
- SQLModel을 사용한 모델 정의
- Base, Table, Create, Update 모델 패턴
- 필드 타입 및 제약 조건

### Step 4: 데이터베이스 연결 및 세션 관리
- 데이터베이스 엔진 생성
- 세션 관리
- 테이블 생성

### Step 5: 데이터 생성 (POST)
- POST 엔드포인트 작성
- 데이터베이스에 데이터 추가
- 세션 커밋 및 리프레시

### Step 6: 데이터 조회 (GET)
- GET 엔드포인트 작성
- 단일 조회 및 목록 조회
- 쿼리 파라미터 사용

### Step 7: 데이터 수정 (PUT)
- PUT 엔드포인트 작성
- 데이터 업데이트 로직
- 부분 업데이트 처리

### Step 8: 데이터 삭제 (DELETE)
- DELETE 엔드포인트 작성
- 데이터 삭제 로직
- 트랜잭션 관리

### Step 9: 테이블 간 관계 (Relationship)
- Foreign Key 설정
- Relationship 정의
- 관계를 통한 데이터 접근

### Step 10: 에러 처리 및 예외 처리
- HTTPException 사용
- 에러 핸들링 패턴
- 트랜잭션 롤백

### Step 11: 라우터 분리 및 구조화
- 라우터를 별도 파일로 분리
- 모듈화된 구조
- 유지보수성 향상

## 실행 방법

각 단계의 디렉토리로 이동한 후:

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 참고사항

- 각 단계는 이전 단계의 내용을 포함하고 있습니다.
- 데이터베이스 연결이 필요한 단계(Step 4 이후)는 PostgreSQL이 필요합니다.
- `.env` 파일을 통해 데이터베이스 연결 정보를 설정하세요.
