"""
POST 라우터: 데이터 생성 관련 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi import Annotated
from sqlmodel import Session
from database import get_session
from models import ItemTable, ItemCreate, ItemResponse


# APIRouter 인스턴스 생성
router = APIRouter(
    prefix="/items",  # 모든 경로에 /items 접두사 추가
    tags=["Items - POST"],  # API 문서에서 그룹화
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: Annotated[ItemCreate, Body(description="생성할 항목 정보")],
    session: Session = Depends(get_session)
):
    """
    새로운 항목을 생성합니다.
    
    Args:
        item: 생성할 항목 정보
        session: 데이터베이스 세션
        
    Returns:
        ItemResponse: 생성된 항목 정보
    """
    try:
        item_orm = ItemTable.model_validate(item)
        session.add(item_orm)
        session.commit()
        session.refresh(item_orm)
        return item_orm
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"항목 생성 중 오류가 발생했습니다: {str(e)}"
        )
