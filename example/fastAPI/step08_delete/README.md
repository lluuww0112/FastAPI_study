# Step 8: 데이터 삭제 (DELETE)

## 학습 목표
- DELETE 요청을 통한 데이터 삭제
- 삭제 전 존재 여부 확인
- 트랜잭션 관리
- 삭제 응답 처리 (204 No Content vs 200 OK)

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

2. 삭제 테스트:
   - **204 응답**: DELETE /items/1 (응답 본문 없음)
   - **200 응답**: DELETE /items/1/with-response (삭제된 항목 정보 반환)

3. 삭제 확인:
   ```bash
   GET /items/1  # 404 에러가 나와야 함
   GET /items/    # 삭제된 항목이 목록에서 제거되었는지 확인
   ```

## 주요 개념

### 삭제 흐름

1. 기본키로 항목 조회
2. 존재 여부 확인 (404 에러 처리)
3. `session.delete(item)` 실행
4. 커밋하여 DB에 반영

### HTTP 상태 코드

- **204 No Content**: 삭제 성공, 응답 본문 없음 (일반적)
- **200 OK**: 삭제 성공, 삭제된 항목 정보 반환 (필요한 경우)
- **404 Not Found**: 삭제할 항목이 없음

### 삭제 응답 패턴

**패턴 1: 204 No Content (권장)**
```python
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(...):
    # 삭제 로직
    return None  # 응답 본문 없음
```

**패턴 2: 200 OK with Response**
```python
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(...):
    # 삭제 로직
    return {"message": "삭제되었습니다"}  # 응답 본문 포함
```

## 주의사항

1. **외래키 제약 조건**: 다른 테이블에서 참조하는 경우 삭제가 실패할 수 있습니다.
   - CASCADE 설정으로 자동 삭제
   - 또는 먼저 참조하는 데이터 삭제

2. **소프트 삭제**: 실제로 삭제하지 않고 `deleted_at` 필드로 표시하는 방법도 있습니다.

3. **트랜잭션 관리**: 오류 발생 시 rollback()을 호출하여 일관성 유지

4. **권한 확인**: 실제 애플리케이션에서는 삭제 권한을 확인해야 합니다.

## 다음 단계

이제 CRUD 작업을 모두 배웠으니, Step 9에서 테이블 간 관계(Relationship)를 학습합니다.
