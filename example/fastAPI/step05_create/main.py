"""
Step 5: 데이터 생성 (POST)

이 예제에서는 POST 요청을 통해 데이터베이스에 데이터를 생성하는 방법을 자세히 학습합니다.
- 요청 바디 검증
- 데이터베이스에 데이터 추가
- 트랜잭션 관리
- 에러 처리
"""

from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi import Annotated
from sqlmodel import Session
from database import create_db_and_tables, get_session
from models import ItemTable, ItemCreate, ItemResponse


app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 5: 데이터 생성 (POST)",
    version="1.0.0",
    lifespan=create_db_and_tables
)


@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: Annotated[ItemCreate, Body(description="생성할 항목 정보")],
    session: Session = Depends(get_session)
):
    """
    새로운 항목을 데이터베이스에 생성합니다.
    
    단계별 설명:
    1. ItemCreate 모델로 요청 바디 검증 (자동으로 FastAPI가 처리)
    2. ItemTable 모델로 변환
    3. 세션에 추가
    4. 커밋하여 실제 DB에 저장
    5. 리프레시하여 생성된 ID 등 최신 정보 반영
    
    Args:
        item: 생성할 항목 정보 (ItemCreate 모델)
        session: 데이터베이스 세션
        
    Returns:
        ItemResponse: 생성된 항목 정보
        
    Raises:
        HTTPException: 데이터베이스 오류 발생 시
    """
    try:
        # 1. Create 모델을 Table 모델로 변환
        # model_validate()를 사용하여 Pydantic 모델을 SQLModel 모델로 변환
        item_orm = ItemTable.model_validate(item)
        
        # 2. 세션에 추가 (아직 DB에 저장되지 않음, 메모리 버퍼에만 존재)
        session.add(item_orm)
        
        # 3. 실제 데이터베이스에 커밋 (저장)
        # commit()을 호출해야만 실제로 DB에 저장됩니다
        session.commit()
        
        # 4. DB에 저장된 후 생성된 ID, created_at 등을 객체에 반영
        # refresh()를 호출하지 않으면 item_orm.item_id가 None일 수 있습니다
        session.refresh(item_orm)
        
        return item_orm
        
    except Exception as e:
        # 오류 발생 시 롤백하여 이전 상태로 복구
        # 여러 테이블을 수정하는 경우, 일부만 성공하고 일부가 실패하면
        # 데이터 일관성이 깨질 수 있으므로 rollback()이 중요합니다
        session.rollback()
        
        print(f"오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"항목 생성 중 오류가 발생했습니다: {str(e)}"
        )


@app.post("/items/batch", response_model=list[ItemResponse], status_code=status.HTTP_201_CREATED)
def create_items_batch(
    items: Annotated[list[ItemCreate], Body(description="생성할 항목 목록")],
    session: Session = Depends(get_session)
):
    """
    여러 항목을 한 번에 생성합니다.
    
    배치 생성의 장점:
    - 여러 항목을 하나의 트랜잭션으로 처리
    - 하나라도 실패하면 모두 롤백되어 데이터 일관성 유지
    
    Args:
        items: 생성할 항목 목록
        session: 데이터베이스 세션
        
    Returns:
        list[ItemResponse]: 생성된 항목 목록
    """
    try:
        # 여러 항목을 리스트로 받아서 처리
        item_orms = [ItemTable.model_validate(item) for item in items]
        
        # 모든 항목을 세션에 추가
        for item_orm in item_orms:
            session.add(item_orm)
        
        # 한 번에 커밋 (모든 항목이 성공해야 저장됨)
        session.commit()
        
        # 모든 항목 리프레시
        for item_orm in item_orms:
            session.refresh(item_orm)
        
        return item_orms
        
    except Exception as e:
        session.rollback()
        print(f"배치 생성 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"항목 배치 생성 중 오류가 발생했습니다: {str(e)}"
        )


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, session: Session = Depends(get_session)):
    """
    생성된 항목을 조회합니다.
    """
    item = session.get(ItemTable, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    return item


# 실행 방법:
# uvicorn main:app --reload
#
# http://localhost:8000/docs 접속하여 테스트해보세요.
# POST /items/ 엔드포인트로 항목을 생성하고,
# GET /items/{item_id} 엔드포인트로 생성된 항목을 확인해보세요.
