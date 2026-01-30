"""
GET 라우터: 데이터 조회 관련 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi import Annotated
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from database import get_session
from models import ItemTable, ItemResponse


router = APIRouter(
    prefix="/items",
    tags=["Items - GET"],
    responses={404: {"description": "Not found"}}
)


class PaginationParams(BaseModel):
    """페이징 파라미터"""
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


@router.get("/", response_model=list[ItemResponse])
def get_items(
    q: Annotated[PaginationParams, Query(description="페이징 파라미터")],
    session: Session = Depends(get_session)
):
    """
    모든 항목을 조회합니다 (페이징 지원).
    
    Args:
        q: 페이징 파라미터
        session: 데이터베이스 세션
        
    Returns:
        list[ItemResponse]: 조회된 항목 목록
    """
    statement = select(ItemTable).offset(q.offset).limit(q.limit)
    results = session.exec(statement).all()
    return results


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: Annotated[int, Path(description="조회할 항목 ID", gt=0)],
    session: Session = Depends(get_session)
):
    """
    특정 항목을 조회합니다.
    
    Args:
        item_id: 조회할 항목 ID
        session: 데이터베이스 세션
        
    Returns:
        ItemResponse: 조회된 항목 정보
    """
    item = session.get(ItemTable, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    return item
