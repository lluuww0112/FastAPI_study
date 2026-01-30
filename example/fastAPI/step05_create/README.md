# Step 5: 데이터 생성 (POST)

## 학습 목표
- POST 요청을 통한 데이터 생성
- 요청 바디 검증 및 모델 변환
- 트랜잭션 관리 (commit, rollback)
- 에러 처리 및 롤백
- 배치 생성 방법

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 테스트 방법

1. http://localhost:8000/docs 접속
2. POST /items/ 엔드포인트 테스트:
   ```json
   {
     "name": "노트북",
     "description": "고성능 노트북",
     "price": 1500000
   }
   ```
3. POST /items/batch 엔드포인트 테스트:
   ```json
   [
     {
       "name": "마우스",
       "description": "무선 마우스",
       "price": 50000
     },
     {
       "name": "키보드",
       "description": "기계식 키보드",
       "price": 150000
     }
   ]
   ```
4. GET /items/{item_id} 엔드포인트로 생성된 항목 확인

## 주요 개념

### 데이터 생성 흐름

1. **요청 바디 검증**: FastAPI가 자동으로 ItemCreate 모델에 맞는지 검증
2. **모델 변환**: `ItemTable.model_validate(item)`로 DB 모델로 변환
3. **세션에 추가**: `session.add(item_orm)` - 메모리 버퍼에 추가
4. **커밋**: `session.commit()` - 실제 DB에 저장
5. **리프레시**: `session.refresh(item_orm)` - 생성된 ID 등 반영

### 트랜잭션 관리

- **트랜잭션**: 여러 작업을 하나의 단위로 묶어서 처리
- **커밋 (Commit)**: 모든 작업이 성공하면 DB에 저장
- **롤백 (Rollback)**: 오류 발생 시 이전 상태로 복구

### 에러 처리

```python
try:
    # 데이터베이스 작업
    session.add(item_orm)
    session.commit()
except Exception as e:
    # 오류 발생 시 롤백
    session.rollback()
    # 에러 응답 반환
    raise HTTPException(...)
```

### 배치 생성

- 여러 항목을 하나의 트랜잭션으로 처리
- 하나라도 실패하면 모두 롤백
- 데이터 일관성 보장

## 주의사항

1. **항상 rollback() 호출**: 예외 발생 시 반드시 rollback()을 호출하여 트랜잭션을 정리해야 합니다.
2. **refresh() 호출**: 생성된 ID나 자동 생성된 필드를 사용하려면 refresh()를 호출해야 합니다.
3. **트랜잭션 범위**: 하나의 요청에서 여러 테이블을 수정하는 경우, 하나의 트랜잭션으로 묶어야 합니다.

## 다음 단계

이제 데이터 생성 방법을 배웠으니, Step 6에서 데이터 조회(GET)를 더 자세히 학습합니다.
