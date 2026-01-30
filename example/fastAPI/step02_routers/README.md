# Step 2: 라우터 기본

## 학습 목표
- APIRouter를 사용한 라우트 그룹화
- 라우터 등록 방법
- 태그를 통한 API 문서 그룹화
- prefix를 통한 경로 관리

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 테스트 방법

1. http://localhost:8000/docs 접속
2. items와 users가 태그별로 그룹화되어 표시되는지 확인
3. 다음 엔드포인트들을 테스트해보세요:
   - GET http://localhost:8000/api/v1/items/
   - GET http://localhost:8000/api/v1/items/1
   - POST http://localhost:8000/api/v1/items/
   - GET http://localhost:8000/api/v1/users/
   - GET http://localhost:8000/api/v1/users/1

## 주요 개념

- **APIRouter**: 관련된 라우트들을 그룹화하는 도구
- **prefix**: 라우터의 모든 경로에 공통으로 붙는 접두사
- **tags**: API 문서에서 엔드포인트를 그룹화하는 태그
- **include_router**: 라우터를 애플리케이션에 등록하는 메서드

## 왜 라우터를 사용하나요?

- 코드를 기능별로 분리하여 가독성 향상
- 대규모 프로젝트에서 코드 관리 용이
- 재사용 가능한 라우터 모듈 생성
- Flask의 Blueprint와 유사한 개념
