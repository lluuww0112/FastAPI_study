"""
PUT 라우터: 데이터 수정 관련 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from fastapi import Annotated
from sqlmodel import Session
from database import get_session
from models import ItemTable, ItemUpdate, ItemResponse


router = APIRouter(
    prefix="/items",
    tags=["Items - PUT"],
    responses={404: {"description": "Not found"}}
)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: Annotated[int, Path(description="수정할 항목 ID", gt=0)],
    item_data: Annotated[ItemUpdate, Body(description="수정할 데이터")],
    session: Session = Depends(get_session)
):
    """
    항목을 부분 업데이트합니다.
    
    Args:
        item_id: 수정할 항목 ID
        item_data: 수정할 데이터
        session: 데이터베이스 세션
        
    Returns:
        ItemResponse: 수정된 항목 정보
    """
    try:
        item = session.get(ItemTable, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item_id} not found"
            )
        
        update_data = item_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"항목 수정 중 오류가 발생했습니다: {str(e)}"
        )
