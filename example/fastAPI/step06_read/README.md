# Step 6: 데이터 조회 (GET)

## 학습 목표
- GET 요청을 통한 데이터 조회
- 단일 항목 조회 (기본키 사용)
- 목록 조회 및 페이징
- 조건부 조회 (where 절)
- 쿼리 파라미터 사용법
- 경로 파라미터 사용법

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 테스트 방법

1. 먼저 테스트 데이터 생성:
   ```bash
   POST /items/
   {
     "name": "노트북",
     "description": "고성능 노트북",
     "price": 1500000
   }
   ```

2. 다양한 조회 방법 테스트:
   - **단일 조회**: GET /items/1
   - **페이징 조회**: GET /items/?offset=0&limit=5
   - **이름으로 검색**: GET /items/search/name/노트북
   - **가격 범위 검색**: GET /items/search/price/?min_price=1000&max_price=100000
   - **전체 개수**: GET /items/count/

## 주요 개념

### 조회 방법

1. **session.get(모델, 기본키)**: 기본키로 단일 객체 조회
   - 가장 빠른 방법
   - 기본키가 아닌 경우 사용 불가

2. **select()**: 복잡한 쿼리 작성
   - 조건부 조회
   - 정렬, 페이징 등

### 쿼리 작성

```python
# 기본 조회
statement = select(ItemTable)

# 조건 추가
statement = select(ItemTable).where(ItemTable.name == "노트북")

# 여러 조건
statement = select(ItemTable).where(
    ItemTable.price >= min_price
).where(
    ItemTable.price <= max_price
)

# 페이징
statement = select(ItemTable).offset(0).limit(10)

# 실행
results = session.exec(statement).all()
```

### 쿼리 파라미터

- `Query()`: 쿼리 파라미터 정의
- `Path()`: 경로 파라미터 정의
- `Annotated`: 타입 힌트와 메타데이터 결합
- `Field()`: Pydantic 모델에서 필드 제약 조건 설정

### 페이징

- **offset**: 건너뛸 항목 수
- **limit**: 반환할 항목 수
- 대용량 데이터를 효율적으로 처리하기 위해 필수

### 에러 처리

- 조회 결과가 없을 때 404 에러 반환
- 적절한 에러 메시지 제공

## 주의사항

1. **페이징 필수**: 대량의 데이터를 한 번에 조회하지 않도록 항상 페이징을 사용하세요.
2. **인덱스 활용**: 자주 검색하는 필드에 인덱스를 추가하면 성능이 향상됩니다.
3. **쿼리 최적화**: 필요한 필드만 조회하도록 쿼리를 최적화하세요.

## 다음 단계

이제 데이터 조회 방법을 배웠으니, Step 7에서 데이터 수정(PUT)을 학습합니다.
