# Step 11: 라우터 분리 및 구조화

## 학습 목표
- 라우터를 별도 파일로 분리하는 방법
- 기능별로 라우터 그룹화
- 메인 앱에서 라우터 등록
- 코드 구조화 및 모듈화
- 유지보수성 향상

## 프로젝트 구조

```
step11_router_separation/
├── main.py              # 메인 애플리케이션
├── database.py          # 데이터베이스 연결
├── models.py            # 데이터 모델
├── requirements.txt     # 의존성
├── README.md           # 설명서
└── routers/            # 라우터 디렉토리
    ├── __init__.py
    ├── post.py         # POST 엔드포인트
    ├── get.py          # GET 엔드포인트
    ├── put.py          # PUT 엔드포인트
    └── delete.py       # DELETE 엔드포인트
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
2. 라우터가 태그별로 그룹화되어 표시되는지 확인
3. 각 엔드포인트 테스트:
   - POST /items/
   - GET /items/
   - GET /items/{item_id}
   - PUT /items/{item_id}
   - DELETE /items/{item_id}

## 주요 개념

### 라우터 분리의 장점

1. **코드 가독성**: 기능별로 분리되어 코드를 이해하기 쉬움
2. **유지보수성**: 특정 기능만 수정할 때 해당 파일만 수정
3. **재사용성**: 라우터를 다른 프로젝트에서 재사용 가능
4. **협업**: 여러 개발자가 동시에 작업하기 쉬움
5. **테스트**: 각 라우터를 독립적으로 테스트 가능

### 라우터 구조

```python
# routers/post.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["Items - POST"]
)

@router.post("/")
def create_item(...):
    ...
```

### 라우터 등록

```python
# main.py
from routers import post, get, put, delete

app.include_router(post.router)
app.include_router(get.router)
app.include_router(put.router)
app.include_router(delete.router)
```

### 태그를 통한 그룹화

- 각 라우터에 `tags`를 설정하면 API 문서에서 그룹화됩니다
- 같은 태그를 사용하면 같은 그룹으로 표시됩니다

## 라우터 분리 패턴

### 패턴 1: HTTP 메서드별 분리 (현재 예제)
- `routers/post.py`: POST 엔드포인트
- `routers/get.py`: GET 엔드포인트
- `routers/put.py`: PUT 엔드포인트
- `routers/delete.py`: DELETE 엔드포인트

### 패턴 2: 리소스별 분리
- `routers/items.py`: Items 관련 모든 엔드포인트
- `routers/users.py`: Users 관련 모든 엔드포인트
- `routers/orders.py`: Orders 관련 모든 엔드포인트

### 패턴 3: 기능별 분리
- `routers/auth.py`: 인증 관련
- `routers/admin.py`: 관리자 관련
- `routers/public.py`: 공개 API

## 주의사항

1. **순환 참조 방지**: 라우터 간 import 시 순환 참조 주의
2. **의존성 관리**: 공통 의존성은 별도 파일로 분리
3. **일관성 유지**: 모든 라우터에서 동일한 패턴 사용
4. **문서화**: 각 라우터 파일에 주석 추가

## 다음 단계

이제 모든 기본 개념을 배웠습니다! 실제 프로젝트에서는:
- 인증/인가 추가
- 미들웨어 사용
- 비동기 처리 최적화
- 테스트 작성
- 배포 설정

등을 추가로 학습하세요.
