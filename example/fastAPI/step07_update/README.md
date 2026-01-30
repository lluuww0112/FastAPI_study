# Step 7: 데이터 수정 (PUT)

## 학습 목표
- PUT 요청을 통한 데이터 수정
- 부분 업데이트 (Partial Update)
- 전체 업데이트
- model_dump()와 exclude_unset 사용법
- setattr()을 통한 동적 속성 업데이트

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

2. 부분 업데이트 테스트:
   ```bash
   PUT /items/1
   {
     "price": 1200000
   }
   ```
   - name과 description은 그대로 유지되고 price만 변경됩니다.

3. 전체 업데이트 테스트:
   ```bash
   PUT /items/1/full
   {
     "name": "데스크탑",
     "description": "고성능 데스크탑",
     "price": 2000000
   }
   ```
   - 모든 필드가 새로운 값으로 교체됩니다.

## 주요 개념

### 부분 업데이트 vs 전체 업데이트

**부분 업데이트 (Partial Update)**
- 클라이언트가 보낸 필드만 업데이트
- `exclude_unset=True` 사용
- RESTful API에서 일반적으로 사용

**전체 업데이트 (Full Update)**
- 모든 필드를 업데이트
- 클라이언트가 보낸 값으로 완전히 교체
- 덜 일반적이지만 필요할 때 사용

### model_dump() 옵션

```python
# exclude_unset=True: 실제로 보낸 필드만 포함 (None이 아닌 값)
update_data = item_data.model_dump(exclude_unset=True)

# exclude_none=True: None 값 제외
update_data = item_data.model_dump(exclude_none=True)

# 모든 필드 포함
update_data = item_data.model_dump()
```

### 동적 속성 업데이트

```python
# setattr()을 사용하여 동적으로 속성 설정
for key, value in update_data.items():
    setattr(item, key, value)
```

### 업데이트 흐름

1. 기본키로 항목 조회
2. 존재 여부 확인 (404 에러 처리)
3. 클라이언트가 보낸 데이터 추출
4. 객체 속성 업데이트
5. 커밋하여 DB에 반영
6. 리프레시하여 최신 정보 반영

## 주의사항

1. **항상 존재 여부 확인**: 업데이트 전에 항목이 존재하는지 확인해야 합니다.
2. **트랜잭션 관리**: 오류 발생 시 rollback()을 호출하여 일관성 유지
3. **부분 업데이트 권장**: RESTful API에서는 일반적으로 부분 업데이트를 사용합니다.
4. **기본키는 수정 불가**: 기본키는 업데이트하지 않도록 주의하세요.

## 다음 단계

이제 데이터 수정 방법을 배웠으니, Step 8에서 데이터 삭제(DELETE)를 학습합니다.
