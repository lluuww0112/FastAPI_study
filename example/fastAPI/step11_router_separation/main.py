"""
Step 11: 라우터 분리 및 구조화

이 예제에서는 라우터를 별도 파일로 분리하여 코드를 구조화하는 방법을 학습합니다.
- 라우터를 별도 파일로 분리
- 기능별로 라우터 그룹화
- 메인 앱에서 라우터 등록
- 코드 가독성 및 유지보수성 향상
"""

from fastapi import FastAPI, Depends
from sqlmodel import Session
from database import create_db_and_tables, get_session

# 라우터들을 import
from routers import post, get, put, delete


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 11: 라우터 분리 및 구조화",
    version="1.0.0",
    lifespan=create_db_and_tables
)


# 라우터들을 애플리케이션에 등록
# include_router를 사용하여 각 라우터를 앱에 추가합니다
app.include_router(post.router)  # POST /items/
app.include_router(get.router)   # GET /items/, GET /items/{item_id}
app.include_router(put.router)   # PUT /items/{item_id}
app.include_router(delete.router) # DELETE /items/{item_id}


# 루트 경로
@app.get("/")
def read_root(session: Session = Depends(get_session)):
    """
    루트 경로
    
    Returns:
        dict: API 정보
    """
    return {
        "message": "FastAPI 라우터 분리 예제",
        "docs": "/docs",
        "endpoints": {
            "POST": "/items/",
            "GET": "/items/",
            "GET_BY_ID": "/items/{item_id}",
            "PUT": "/items/{item_id}",
            "DELETE": "/items/{item_id}"
        }
    }


# 헬스 체크 엔드포인트
@app.get("/health")
def health_check(session: Session = Depends(get_session)):
    """
    서버 상태 확인
    
    Returns:
        dict: 서버 상태
    """
    return {"status": "ok"}


# 실행 방법:
# uvicorn main:app --reload
#
# http://localhost:8000/docs 접속하면
# 라우터가 태그별로 그룹화되어 표시됩니다.
#
# 프로젝트 구조:
# step11_router_separation/
# ├── main.py              # 메인 애플리케이션
# ├── database.py          # 데이터베이스 연결
# ├── models.py            # 데이터 모델
# └── routers/             # 라우터 디렉토리
#     ├── __init__.py
#     ├── post.py          # POST 엔드포인트
#     ├── get.py           # GET 엔드포인트
#     ├── put.py           # PUT 엔드포인트
#     └── delete.py        # DELETE 엔드포인트
