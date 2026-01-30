"""
Step 1: FastAPI 기본

이 예제에서는 FastAPI의 기본 사용법을 학습합니다.
- FastAPI 애플리케이션 생성
- 기본 라우트 정의
- 실행 방법
"""

from fastapi import FastAPI

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 1: FastAPI 기본 사용법",
    version="1.0.0"
)


# 기본 라우트 정의
# @app.get() 데코레이터를 사용하여 GET 요청을 처리하는 엔드포인트를 정의합니다
@app.get("/")
def read_root():
    """
    루트 경로에 대한 GET 요청을 처리합니다.
    
    Returns:
        dict: 간단한 인사 메시지
    """
    return {"message": "Hello, FastAPI!"}


# 경로 파라미터 사용
@app.get("/hello/{name}")
def hello_name(name: str):
    """
    경로에 포함된 이름을 받아 인사 메시지를 반환합니다.
    
    Args:
        name: 경로에서 추출한 이름
        
    Returns:
        dict: 이름을 포함한 인사 메시지
    """
    return {"message": f"Hello, {name}!"}


# 쿼리 파라미터 사용
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    """
    쿼리 파라미터를 사용하여 데이터를 조회합니다.
    
    Args:
        skip: 건너뛸 항목 수 (기본값: 0)
        limit: 반환할 항목 수 (기본값: 10)
        
    Returns:
        dict: 쿼리 파라미터 정보
    """
    return {
        "skip": skip,
        "limit": limit,
        "message": f"skip={skip}, limit={limit}인 항목들을 조회합니다"
    }


# POST 요청 처리
@app.post("/items/")
def create_item(name: str, description: str = None):
    """
    POST 요청을 통해 새로운 항목을 생성합니다.
    
    Args:
        name: 항목 이름
        description: 항목 설명 (선택사항)
        
    Returns:
        dict: 생성된 항목 정보
    """
    return {
        "name": name,
        "description": description,
        "message": "항목이 생성되었습니다"
    }


# 실행 방법:
# uvicorn main:app --reload
# 
# 브라우저에서 http://localhost:8000/docs 접속하면 자동 생성된 API 문서를 확인할 수 있습니다.
