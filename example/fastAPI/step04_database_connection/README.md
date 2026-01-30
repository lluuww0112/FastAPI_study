# Step 4: 데이터베이스 연결 및 세션 관리

## 학습 목표
- 데이터베이스 엔진 생성 방법
- 세션 관리 및 의존성 주입
- 테이블 자동 생성
- 데이터베이스에 데이터 추가 및 조회

## 사전 준비

### PostgreSQL 설치 및 실행

1. PostgreSQL이 설치되어 있어야 합니다.
2. 데이터베이스 생성:
   ```sql
   CREATE DATABASE testdb;
   ```

### 환경 변수 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하거나 환경 변수를 설정하세요.

```bash
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=testdb
export DB_HOST=localhost
export DB_PORT=5432
```

또는 `.env` 파일을 생성:
```bash
cp .env.example .env
# .env 파일을 편집하여 실제 값 입력
```

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 테스트 방법

1. http://localhost:8000/docs 접속
2. 서버 시작 시 콘솔에 "데이터베이스 테이블을 생성합니다..." 메시지 확인
3. 다음 엔드포인트들을 테스트해보세요:
   - POST http://localhost:8000/items/ (body에 name, description, price 포함)
   - GET http://localhost:8000/items/1
   - GET http://localhost:8000/items/ (쿼리 파라미터: skip=0, limit=10)

## 주요 개념

### 데이터베이스 엔진

- `create_engine()`: 데이터베이스 연결을 관리하는 엔진 생성
- `echo=True`: SQL 쿼리를 콘솔에 출력 (디버깅용)

### 세션 관리

- `Session`: 데이터베이스와의 통신을 위한 세션 객체
- `Depends(get_session)`: FastAPI의 의존성 주입을 통한 세션 자동 관리
- `with Session()`: 세션 자동 종료 보장

### 데이터베이스 작업 흐름

1. **추가 (Add)**: `session.add(객체)` - 세션에 객체 추가
2. **커밋 (Commit)**: `session.commit()` - 실제 DB에 저장
3. **리프레시 (Refresh)**: `session.refresh(객체)` - DB에서 최신 정보 가져오기

### 쿼리 작성

- `session.get(모델, 기본키)`: 기본키로 단일 객체 조회
- `select(모델)`: 쿼리 생성
- `session.exec(statement)`: 쿼리 실행

### Lifespan

- `lifespan`: 서버 시작/종료 시 실행할 함수 등록
- `@asynccontextmanager`: 비동기 컨텍스트 매니저
- 서버 시작 시 테이블 자동 생성

## SQLite 사용하기 (학습용)

PostgreSQL 대신 SQLite를 사용하려면 `database.py`에서 다음처럼 변경:

```python
SQLITE_URL = "sqlite:///./example.db"
engine = create_engine(SQLITE_URL, echo=True)
```

SQLite는 파일 기반 데이터베이스이므로 별도 설치가 필요 없습니다.

## 다음 단계

이제 데이터베이스 연결을 배웠으니, Step 5에서 데이터 생성(POST)을 더 자세히 학습합니다.
