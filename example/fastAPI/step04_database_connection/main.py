"""
Step 4: 데이터베이스 연결 및 세션 관리

이 예제에서는 데이터베이스에 연결하고 세션을 사용하는 방법을 학습합니다.
"""

from fastapi import FastAPI, Depends
from sqlmodel import Session
from database import create_db_and_tables, get_session
from models import ItemTable, ItemCreate, ItemUpdate


# lifespan에 create_db_and_tables를 등록하여 서버 시작 시 테이블 생성
app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 4: 데이터베이스 연결 및 세션 관리",
    version="1.0.0",
    lifespan=create_db_and_tables  # 서버 시작/종료 시 실행할 함수
)


@app.get("/")
def read_root():
    """
    루트 경로
    """
    return {
        "message": "데이터베이스 연결 예제",
        "docs": "/docs"
    }


@app.post("/items/", response_model=ItemTable)
def create_item(
    item: ItemCreate,
    session: Session = Depends(get_session)  # 세션을 의존성 주입으로 받음
):
    """
    데이터베이스에 새로운 항목을 생성합니다.
    
    Args:
        item: ItemCreate 모델로 받은 데이터
        session: 데이터베이스 세션
        
    Returns:
        ItemTable: 생성된 항목 정보
    """
    # 1. Create 모델을 Table 모델로 변환
    item_orm = ItemTable.model_validate(item)
    
    # 2. 세션에 추가 (아직 DB에 저장되지 않음)
    session.add(item_orm)
    
    # 3. 실제 데이터베이스에 커밋 (저장)
    session.commit()
    
    # 4. DB에 저장된 후 생성된 ID 등을 객체에 반영
    session.refresh(item_orm)
    
    return item_orm


@app.get("/items/{item_id}", response_model=ItemTable)
def get_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    """
    데이터베이스에서 항목을 조회합니다.
    
    Args:
        item_id: 조회할 항목 ID
        session: 데이터베이스 세션
        
    Returns:
        ItemTable: 조회된 항목 정보
    """
    # session.get()을 사용하여 기본키로 조회
    item = session.get(ItemTable, item_id)
    
    if not item:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    return item


@app.get("/items/", response_model=list[ItemTable])
def get_items(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    """
    데이터베이스에서 모든 항목을 조회합니다.
    
    Args:
        skip: 건너뛸 항목 수
        limit: 반환할 항목 수
        session: 데이터베이스 세션
        
    Returns:
        list[ItemTable]: 조회된 항목 목록
    """
    from sqlmodel import select
    
    # select()를 사용하여 쿼리 생성
    statement = select(ItemTable).offset(skip).limit(limit)
    
    # 쿼리 실행
    results = session.exec(statement).all()
    
    return results


# 실행 방법:
# 1. 데이터베이스 설정 (.env 파일 또는 환경 변수)
# 2. uvicorn main:app --reload
#
# http://localhost:8000/docs 접속하여 테스트해보세요.
