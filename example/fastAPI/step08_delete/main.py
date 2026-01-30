"""
Step 8: 데이터 삭제 (DELETE)

이 예제에서는 DELETE 요청을 통해 데이터베이스에서 데이터를 삭제하는 방법을 자세히 학습합니다.
- 단일 항목 삭제
- 삭제 전 존재 여부 확인
- 트랜잭션 관리
- 삭제 응답 처리
"""

from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi import Annotated
from sqlmodel import Session
from database import create_db_and_tables, get_session
from models import ItemTable, ItemCreate, ItemResponse


app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 8: 데이터 삭제 (DELETE)",
    version="1.0.0",
    lifespan=create_db_and_tables
)


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: Annotated[int, Path(description="삭제할 항목 ID", gt=0)],
    session: Session = Depends(get_session)
):
    """
    항목을 삭제합니다.
    
    단계별 설명:
    1. 기본키로 항목 조회
    2. 존재 여부 확인
    3. 삭제 실행
    4. 커밋하여 DB에 반영
    
    주의사항:
    - DELETE 요청은 일반적으로 응답 본문이 없습니다 (204 No Content)
    - 외래키 제약 조건이 있는 경우 CASCADE 설정 확인 필요
    
    Args:
        item_id: 삭제할 항목 ID
        session: 데이터베이스 세션
        
    Raises:
        HTTPException: 항목을 찾을 수 없는 경우 404 에러
    """
    try:
        # 1. 기본키로 항목 조회
        item = session.get(ItemTable, item_id)
        
        # 2. 존재 여부 확인
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item_id} not found"
            )
        
        # 3. 삭제 실행
        session.delete(item)
        
        # 4. 커밋하여 DB에 반영
        session.commit()
        
        # 204 No Content는 응답 본문이 없습니다
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"삭제 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"항목 삭제 중 오류가 발생했습니다: {str(e)}"
        )


@app.delete("/items/{item_id}/with-response", response_model=dict)
def delete_item_with_response(
    item_id: Annotated[int, Path(description="삭제할 항목 ID", gt=0)],
    session: Session = Depends(get_session)
):
    """
    항목을 삭제하고 삭제된 항목 정보를 반환합니다.
    
    경우에 따라 삭제된 항목 정보를 반환해야 할 수도 있습니다.
    이 경우 200 OK와 함께 삭제된 항목 정보를 반환합니다.
    
    Args:
        item_id: 삭제할 항목 ID
        session: 데이터베이스 세션
        
    Returns:
        dict: 삭제된 항목 정보
    """
    try:
        item = session.get(ItemTable, item_id)
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item_id} not found"
            )
        
        # 삭제 전 정보 저장
        deleted_item_info = {
            "item_id": item.item_id,
            "name": item.name,
            "message": f"'{item.name}' 항목이 삭제되었습니다"
        }
        
        session.delete(item)
        session.commit()
        
        return deleted_item_info
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"항목 삭제 중 오류가 발생했습니다: {str(e)}"
        )


# 테스트용 엔드포인트들
@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    """테스트용 데이터 생성"""
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


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, session: Session = Depends(get_session)):
    """항목 조회"""
    item = session.get(ItemTable, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    return item


@app.get("/items/", response_model=list[ItemResponse])
def get_items(session: Session = Depends(get_session)):
    """모든 항목 조회"""
    from sqlmodel import select
    statement = select(ItemTable)
    results = session.exec(statement).all()
    return results


# 실행 방법:
# uvicorn main:app --reload
#
# http://localhost:8000/docs 접속하여 테스트해보세요.
# 1. 먼저 POST /items/로 항목 생성
# 2. GET /items/로 생성된 항목 확인
# 3. DELETE /items/{item_id}로 항목 삭제
# 4. GET /items/로 삭제 확인
