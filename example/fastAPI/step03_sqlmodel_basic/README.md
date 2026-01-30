# Step 3: SQLModel 기본 모델 정의

## 학습 목표
- SQLModel을 사용한 모델 정의 방법
- Base, Table, Create, Update 모델 패턴 이해
- 필드 타입 및 제약 조건 설정
- FastAPI에서 모델 사용 방법

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 테스트 방법

1. http://localhost:8000/docs 접속
2. 자동 생성된 스키마 확인
3. 다음 엔드포인트들을 테스트해보세요:
   - POST http://localhost:8000/items/ (body에 name, description, price 포함)
   - GET http://localhost:8000/items/1
   - PUT http://localhost:8000/items/1 (body에 수정할 필드 포함)

## 주요 개념

### 모델 패턴

1. **Base 모델**: 공통 필드 정의
   - 모든 관련 모델이 공유하는 필드
   - 주로 Not Null 필드들로 구성

2. **Table 모델**: 데이터베이스 테이블 정의
   - `table=True` 설정 필요
   - 기본키, 외래키, 인덱스 등 DB 제약 조건 설정

3. **Create 모델**: 데이터 생성 시 사용
   - 클라이언트가 보내는 데이터 구조
   - Base를 상속받아 추가 필드 정의

4. **Update 모델**: 데이터 수정 시 사용
   - 모든 필드를 Optional로 정의
   - 부분 업데이트 가능

### 필드 타입

- `str`: 문자열 (Not Null)
- `Optional[str]`: 문자열 (Nullable)
- `int`: 정수 (Not Null)
- `Optional[int]`: 정수 (Nullable)
- `datetime`: 날짜/시간
- `Field()`: 제약 조건 설정 (primary_key, unique, default 등)

### Field 옵션

- `primary_key=True`: 기본키 설정
- `unique=True`: 유일값 제약
- `default=값`: 기본값 설정
- `default_factory=함수`: 함수로 기본값 생성

## 다음 단계

이제 모델을 정의했으니, Step 4에서 실제 데이터베이스에 연결하는 방법을 학습합니다.
