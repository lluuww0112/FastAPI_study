"""
Step 6: 데이터 조회 (GET)

이 예제에서는 GET 요청을 통해 데이터베이스에서 데이터를 조회하는 방법을 자세히 학습합니다.
- 단일 항목 조회
- 목록 조회 (페이징)
- 조건부 조회
- 쿼리 파라미터 사용
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from fastapi import Annotated
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import ItemTable, ItemCreate, ItemResponse


app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 6: 데이터 조회 (GET)",
    version="1.0.0",
    lifespan=create_db_and_tables
)


# 쿼리 파라미터를 위한 모델 정의
class PaginationParams(BaseModel):
    """페이징을 위한 쿼리 파라미터"""
    offset: int = Field(default=0, ge=0, description="건너뛸 항목 수")
    limit: int = Field(default=10, ge=1, le=100, description="반환할 항목 수")


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: Annotated[int, Path(description="조회할 항목 ID", gt=0)],
    session: Session = Depends(get_session)
):
    """
    기본키를 사용하여 단일 항목을 조회합니다.
    
    Args:
        item_id: 조회할 항목 ID (경로 파라미터)
        session: 데이터베이스 세션
        
    Returns:
        ItemResponse: 조회된 항목 정보
        
    Raises:
        HTTPException: 항목을 찾을 수 없는 경우 404 에러
    """
    # session.get()을 사용하여 기본키로 조회
    # 기본키가 아닌 경우 select()를 사용해야 합니다
    item = session.get(ItemTable, item_id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    return item


@app.get("/items/", response_model=list[ItemResponse])
def get_items(
    q: Annotated[PaginationParams, Query(description="페이징 파라미터")],
    session: Session = Depends(get_session)
):
    """
    모든 항목을 조회합니다 (페이징 지원).
    
    Args:
        q: 페이징 파라미터 (offset, limit)
        session: 데이터베이스 세션
        
    Returns:
        list[ItemResponse]: 조회된 항목 목록
    """
    # select()를 사용하여 쿼리 생성
    statement = (
        select(ItemTable)
        .offset(q.offset)  # 건너뛸 항목 수
        .limit(q.limit)    # 반환할 항목 수
    )
    
    # 쿼리 실행
    results = session.exec(statement).all()
    
    return results


@app.get("/items/search/name/{name}", response_model=list[ItemResponse])
def get_items_by_name(
    name: Annotated[str, Path(description="검색할 이름")],
    session: Session = Depends(get_session)
):
    """
    이름으로 항목을 검색합니다.
    
    Args:
        name: 검색할 이름
        session: 데이터베이스 세션
        
    Returns:
        list[ItemResponse]: 검색된 항목 목록
    """
    # where 절을 사용하여 조건부 조회
    statement = select(ItemTable).where(ItemTable.name == name)
    
    results = session.exec(statement).all()
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"'{name}' 이름을 가진 항목을 찾을 수 없습니다"
        )
    
    return results


@app.get("/items/search/price/", response_model=list[ItemResponse])
def get_items_by_price_range(
    min_price: Annotated[float, Query(description="최소 가격", ge=0)] = 0,
    max_price: Annotated[float, Query(description="최대 가격", ge=0)] = None,
    session: Session = Depends(get_session)
):
    """
    가격 범위로 항목을 검색합니다.
    
    Args:
        min_price: 최소 가격
        max_price: 최대 가격 (None이면 제한 없음)
        session: 데이터베이스 세션
        
    Returns:
        list[ItemResponse]: 검색된 항목 목록
    """
    # 기본 쿼리 생성
    statement = select(ItemTable).where(ItemTable.price >= min_price)
    
    # 최대 가격이 지정된 경우 추가 조건
    if max_price is not None:
        statement = statement.where(ItemTable.price <= max_price)
    
    results = session.exec(statement).all()
    
    return results


@app.get("/items/count/", response_model=dict)
def get_items_count(session: Session = Depends(get_session)):
    """
    전체 항목 수를 조회합니다.
    
    Args:
        session: 데이터베이스 세션
        
    Returns:
        dict: 항목 수 정보
    """
    # count()를 사용하여 개수 조회
    statement = select(ItemTable)
    count = len(session.exec(statement).all())
    
    return {"total_count": count}


# 테스트용 데이터 생성 엔드포인트
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


# 실행 방법:
# uvicorn main:app --reload
#
# http://localhost:8000/docs 접속하여 테스트해보세요.
# 다양한 조회 방법을 시도해보세요:
# - GET /items/1 (단일 조회)
# - GET /items/?offset=0&limit=5 (페이징)
# - GET /items/search/name/노트북 (이름으로 검색)
# - GET /items/search/price/?min_price=1000&max_price=100000 (가격 범위 검색)
