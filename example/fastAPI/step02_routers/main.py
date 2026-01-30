"""
Step 2: 라우터 기본

이 예제에서는 FastAPI의 APIRouter를 사용하는 방법을 학습합니다.
- APIRouter 생성 및 사용
- 라우터 등록
- 태그 및 설명 추가
"""

from fastapi import FastAPI, APIRouter

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 2: 라우터 기본 사용법",
    version="1.0.0"
)

# APIRouter 인스턴스 생성
# prefix: 모든 라우트에 공통으로 붙는 경로
# tags: API 문서에서 그룹화할 태그
router = APIRouter(
    prefix="/api/v1",
    tags=["items"],  # API 문서에서 "items" 태그로 그룹화됨
    responses={404: {"description": "Not found"}}  # 기본 응답 정의
)


# 라우터에 엔드포인트 정의
@router.get("/items/")
def get_items():
    """
    모든 항목을 조회합니다.
    """
    return {"items": ["item1", "item2", "item3"]}


@router.get("/items/{item_id}")
def get_item(item_id: int):
    """
    특정 항목을 조회합니다.
    
    Args:
        item_id: 항목 ID
    """
    return {"item_id": item_id, "name": f"item{item_id}"}


@router.post("/items/")
def create_item(name: str, description: str = None):
    """
    새로운 항목을 생성합니다.
    
    Args:
        name: 항목 이름
        description: 항목 설명
    """
    return {
        "name": name,
        "description": description,
        "message": "항목이 생성되었습니다"
    }


# 또 다른 라우터 생성 (다른 기능 그룹)
users_router = APIRouter(
    prefix="/api/v1",
    tags=["users"],  # 다른 태그로 그룹화
)


@users_router.get("/users/")
def get_users():
    """
    모든 사용자를 조회합니다.
    """
    return {"users": ["user1", "user2"]}


@users_router.get("/users/{user_id}")
def get_user(user_id: int):
    """
    특정 사용자를 조회합니다.
    
    Args:
        user_id: 사용자 ID
    """
    return {"user_id": user_id, "name": f"user{user_id}"}


# 애플리케이션에 라우터 등록
# include_router를 사용하여 라우터를 앱에 추가합니다
app.include_router(router)
app.include_router(users_router)


# 루트 경로는 직접 앱에 정의 가능
@app.get("/")
def read_root():
    """
    루트 경로
    """
    return {
        "message": "FastAPI 라우터 예제",
        "docs": "/docs",
        "items": "/api/v1/items/",
        "users": "/api/v1/users/"
    }


# 실행 방법:
# uvicorn main:app --reload
#
# 브라우저에서 http://localhost:8000/docs 접속하면
# items와 users가 태그별로 그룹화되어 표시됩니다.
