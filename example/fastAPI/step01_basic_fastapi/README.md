# Step 1: FastAPI 기본

## 학습 목표
- FastAPI 애플리케이션 생성 방법
- 기본 라우트 정의 방법
- GET, POST 요청 처리 방법
- 경로 파라미터와 쿼리 파라미터 사용법

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 테스트 방법

1. 브라우저에서 http://localhost:8000 접속
2. http://localhost:8000/docs 접속하여 자동 생성된 API 문서 확인
3. 다음 엔드포인트들을 테스트해보세요:
   - GET http://localhost:8000/
   - GET http://localhost:8000/hello/홍길동
   - GET http://localhost:8000/items/?skip=0&limit=5
   - POST http://localhost:8000/items/ (name과 description을 body에 포함)

## 주요 개념

- **FastAPI**: 현대적인 Python 웹 프레임워크
- **라우트**: URL 경로와 함수를 연결하는 방법
- **경로 파라미터**: URL 경로에 포함된 변수 (예: `/hello/{name}`)
- **쿼리 파라미터**: URL 뒤에 `?`로 시작하는 파라미터 (예: `?skip=0&limit=10`)
- **자동 문서화**: FastAPI는 자동으로 OpenAPI 문서를 생성합니다
