# Step 10: 에러 처리 및 예외 처리

## 학습 목표
- HTTPException 사용법
- 커스텀 예외 클래스 정의
- 예외 처리기 (Exception Handler) 구현
- 트랜잭션 롤백 처리
- 에러 응답 포맷 통일

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 테스트 방법

1. **404 에러 테스트**:
   ```bash
   GET /items/999  # 존재하지 않는 항목
   ```

2. **409 에러 테스트**:
   ```bash
   POST /items/
   {
     "name": "노트북",
     "price": 1000
   }
   # 같은 이름으로 다시 생성 시도
   ```

3. **422 에러 테스트**:
   ```bash
   POST /items/
   {
     "name": 123  # 잘못된 타입
   }
   ```

4. **500 에러 테스트**:
   - 데이터베이스 연결 오류 등

## 주요 개념

### HTTPException

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found"
)
```

- FastAPI의 기본 예외 클래스
- HTTP 상태 코드와 메시지 지정
- 자동으로 JSON 응답으로 변환

### 커스텀 예외 클래스

```python
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.message = f"Item {item_id} not found"
```

- 비즈니스 로직에 맞는 예외 정의
- 더 명확한 에러 메시지
- 예외 처리기로 중앙 관리

### 예외 처리기 (Exception Handler)

```python
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Item Not Found", "message": exc.message}
    )
```

- 특정 예외를 중앙에서 처리
- 일관된 에러 응답 포맷
- 여러 엔드포인트에서 재사용

### 에러 처리 패턴

1. **명시적 체크**: 조건 확인 후 HTTPException 발생
2. **예외 전파**: 예외를 핸들러로 전달
3. **롤백**: 데이터베이스 작업 실패 시 rollback()

### 트랜잭션 롤백

```python
try:
    # 데이터베이스 작업
    session.add(item)
    session.commit()
except Exception as e:
    session.rollback()  # 이전 상태로 복구
    raise
```

- 오류 발생 시 이전 상태로 복구
- 데이터 일관성 유지

## HTTP 상태 코드

- **200 OK**: 성공
- **201 Created**: 생성 성공
- **204 No Content**: 삭제 성공 (응답 본문 없음)
- **400 Bad Request**: 잘못된 요청
- **404 Not Found**: 리소스를 찾을 수 없음
- **409 Conflict**: 충돌 (중복 등)
- **422 Unprocessable Entity**: 검증 오류
- **500 Internal Server Error**: 서버 오류

## 주의사항

1. **민감한 정보 노출 방지**: 프로덕션에서는 상세한 에러 정보를 숨기세요.
2. **일관된 에러 포맷**: 모든 에러 응답을 통일된 형식으로 반환하세요.
3. **롤백 필수**: 데이터베이스 작업 실패 시 반드시 rollback()을 호출하세요.
4. **로깅**: 에러 발생 시 로그를 남겨 디버깅에 활용하세요.

## 다음 단계

이제 에러 처리를 배웠으니, Step 11에서 라우터 분리 및 구조화를 학습합니다.
