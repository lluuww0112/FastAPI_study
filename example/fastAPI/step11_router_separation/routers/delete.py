"""
DELETE 라우터: 데이터 삭제 관련 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi import Annotated
from sqlmodel import Session
from database import get_session
from models import ItemTable


router = APIRouter(
    prefix="/items",
    tags=["Items - DELETE"],
    responses={404: {"description": "Not found"}}
)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: Annotated[int, Path(description="삭제할 항목 ID", gt=0)],
    session: Session = Depends(get_session)
):
    """
    항목을 삭제합니다.
    
    Args:
        item_id: 삭제할 항목 ID
        session: 데이터베이스 세션
        
    Returns:
        None: 204 No Content
    """
    try:
        item = session.get(ItemTable, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item_id} not found"
            )
        
        session.delete(item)
        session.commit()
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"항목 삭제 중 오류가 발생했습니다: {str(e)}"
        )
