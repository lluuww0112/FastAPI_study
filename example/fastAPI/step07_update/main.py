"""
Step 7: 데이터 수정 (PUT)

이 예제에서는 PUT 요청을 통해 데이터베이스의 데이터를 수정하는 방법을 자세히 학습합니다.
- 부분 업데이트 (Partial Update)
- 전체 업데이트
- 업데이트 전 존재 여부 확인
- 트랜잭션 관리
"""

from fastapi import FastAPI, Depends, HTTPException, status, Path, Body
from fastapi import Annotated
from sqlmodel import Session
from database import create_db_and_tables, get_session
from models import ItemTable, ItemCreate, ItemUpdate, ItemResponse


app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 7: 데이터 수정 (PUT)",
    version="1.0.0",
    lifespan=create_db_and_tables
)


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: Annotated[int, Path(description="수정할 항목 ID", gt=0)],
    item_data: Annotated[ItemUpdate, Body(description="수정할 데이터")],
    session: Session = Depends(get_session)
):
    """
    항목을 부분 업데이트합니다.
    
    부분 업데이트란:
    - 클라이언트가 보낸 필드만 업데이트
    - None인 필드는 업데이트하지 않음
    - 기존 값은 그대로 유지
    
    단계별 설명:
    1. 기본키로 항목 조회
    2. 존재 여부 확인
    3. 클라이언트가 보낸 데이터만 추출 (exclude_unset=True)
    4. 객체 속성 업데이트
    5. 커밋하여 DB에 반영
    
    Args:
        item_id: 수정할 항목 ID
        item_data: 수정할 데이터 (ItemUpdate 모델)
        session: 데이터베이스 세션
        
    Returns:
        ItemResponse: 수정된 항목 정보
        
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
        
        # 3. 클라이언트가 보낸 데이터만 추출
        # exclude_unset=True: None이 아닌 값만 포함 (실제로 보낸 필드만)
        # exclude_none=True: None 값 제외 (None을 명시적으로 보낸 경우도 제외)
        update_data = item_data.model_dump(exclude_unset=True)
        
        # 4. 객체 속성 업데이트
        # setattr()을 사용하여 동적으로 속성 설정
        for key, value in update_data.items():
            setattr(item, key, value)
        
        # 5. 커밋하여 DB에 반영
        session.add(item)  # 명시적으로 추가 (변경사항 추적)
        session.commit()
        session.refresh(item)  # 최신 정보 반영
        
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"업데이트 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"항목 수정 중 오류가 발생했습니다: {str(e)}"
        )


@app.put("/items/{item_id}/full", response_model=ItemResponse)
def update_item_full(
    item_id: Annotated[int, Path(description="수정할 항목 ID", gt=0)],
    item_data: Annotated[ItemCreate, Body(description="전체 데이터")],
    session: Session = Depends(get_session)
):
    """
    항목을 전체 업데이트합니다.
    
    전체 업데이트란:
    - 모든 필드를 업데이트
    - 클라이언트가 보낸 값으로 완전히 교체
    
    Args:
        item_id: 수정할 항목 ID
        item_data: 전체 데이터 (ItemCreate 모델)
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
        
        # 전체 데이터로 업데이트
        update_data = item_data.model_dump()
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


# 실행 방법:
# uvicorn main:app --reload
#
# http://localhost:8000/docs 접속하여 테스트해보세요.
# 1. 먼저 POST /items/로 항목 생성
# 2. PUT /items/{item_id}로 부분 업데이트 (일부 필드만 수정)
# 3. PUT /items/{item_id}/full로 전체 업데이트
