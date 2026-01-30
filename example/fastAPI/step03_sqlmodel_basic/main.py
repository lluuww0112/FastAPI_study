"""
Step 3: SQLModel 기본 모델 정의

이 예제에서는 정의한 모델을 FastAPI에서 사용하는 방법을 보여줍니다.
실제 데이터베이스 연결은 Step 4에서 학습합니다.
"""

from fastapi import FastAPI
from models import ItemCreate, ItemUpdate, ItemResponse

app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 3: SQLModel 기본 모델 정의",
    version="1.0.0"
)


@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    """
    ItemCreate 모델을 사용하여 항목을 생성합니다.
    (실제 데이터베이스 저장은 Step 4에서 학습)
    
    Args:
        item: ItemCreate 모델로 받은 데이터
        
    Returns:
        ItemResponse: 생성된 항목 정보
    """
    # 실제로는 데이터베이스에 저장하지만,
    # 여기서는 예시로 메모리에 저장합니다
    return {
        "item_id": 1,
        "name": item.name,
        "description": item.description,
        "price": item.price or 0.0,
        "created_at": "2024-01-01T00:00:00"
    }


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate):
    """
    ItemUpdate 모델을 사용하여 항목을 수정합니다.
    
    Args:
        item_id: 수정할 항목 ID
        item: ItemUpdate 모델로 받은 수정 데이터
        
    Returns:
        ItemResponse: 수정된 항목 정보
    """
    # 실제로는 데이터베이스에서 조회 후 수정하지만,
    # 여기서는 예시로 반환합니다
    return {
        "item_id": item_id,
        "name": item.name or "기본 이름",
        "description": item.description,
        "price": item.price or 0.0,
        "created_at": "2024-01-01T00:00:00"
    }


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    """
    항목을 조회합니다.
    
    Args:
        item_id: 조회할 항목 ID
        
    Returns:
        ItemResponse: 조회된 항목 정보
    """
    return {
        "item_id": item_id,
        "name": "예시 항목",
        "description": "예시 설명",
        "price": 1000.0,
        "created_at": "2024-01-01T00:00:00"
    }


# 실행 방법:
# uvicorn main:app --reload
#
# http://localhost:8000/docs 접속하여
# 자동 생성된 스키마를 확인해보세요.
# FastAPI가 모델을 기반으로 자동으로 API 문서를 생성합니다.
