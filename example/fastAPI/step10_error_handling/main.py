"""
Step 10: 에러 처리 및 예외 처리

이 예제에서는 FastAPI에서 에러를 처리하는 다양한 방법을 학습합니다.
- HTTPException 사용
- 커스텀 예외 처리기
- 트랜잭션 롤백
- 에러 응답 포맷 통일
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlmodel import Session, IntegrityError
from database import create_db_and_tables, get_session
from models import ItemTable, ItemCreate, ItemUpdate, ItemResponse
import traceback


app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 10: 에러 처리 및 예외 처리",
    version="1.0.0",
    lifespan=create_db_and_tables
)


# ========== 커스텀 예외 클래스 ==========

class ItemNotFoundError(Exception):
    """항목을 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.message = f"Item {item_id} not found"


class DuplicateItemError(Exception):
    """중복된 항목이 있을 때 발생하는 예외"""
    def __init__(self, name: str):
        self.name = name
        self.message = f"Item with name '{name}' already exists"


# ========== 커스텀 예외 처리기 ==========

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    """ItemNotFoundError를 처리하는 커스텀 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Item Not Found",
            "message": exc.message,
            "item_id": exc.item_id
        }
    )


@app.exception_handler(DuplicateItemError)
async def duplicate_item_handler(request: Request, exc: DuplicateItemError):
    """DuplicateItemError를 처리하는 커스텀 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Duplicate Item",
            "message": exc.message,
            "item_name": exc.name
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """요청 검증 오류를 처리하는 커스텀 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "입력 데이터가 올바르지 않습니다",
            "details": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """일반적인 예외를 처리하는 핸들러"""
    # 개발 환경에서만 상세한 에러 정보 반환
    import os
    if os.getenv("ENV", "dev") == "dev":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": str(exc),
                "traceback": traceback.format_exc()
            }
        )
    else:
        # 프로덕션 환경에서는 상세 정보 숨김
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "서버에서 오류가 발생했습니다"
            }
        )


# ========== 엔드포인트 ==========

@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    """
    항목을 생성합니다.
    
    다양한 에러 처리 방법을 보여줍니다:
    1. HTTPException 직접 사용
    2. 커스텀 예외 사용
    3. 데이터베이스 제약 조건 오류 처리
    """
    try:
        # 중복 체크
        from sqlmodel import select
        existing_item = session.exec(
            select(ItemTable).where(ItemTable.name == item.name)
        ).first()
        
        if existing_item:
            # 방법 1: 커스텀 예외 사용
            raise DuplicateItemError(item.name)
        
        item_orm = ItemTable.model_validate(item)
        session.add(item_orm)
        session.commit()
        session.refresh(item_orm)
        return item_orm
        
    except DuplicateItemError:
        # 커스텀 예외는 핸들러가 처리
        raise
    except IntegrityError as e:
        # 데이터베이스 제약 조건 오류
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"데이터베이스 제약 조건 위반: {str(e)}"
        )
    except Exception as e:
        session.rollback()
        # 일반 예외는 핸들러가 처리
        raise


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, session: Session = Depends(get_session)):
    """
    항목을 조회합니다.
    
    에러 처리 방법:
    1. HTTPException 직접 사용
    2. 커스텀 예외 사용
    """
    item = session.get(ItemTable, item_id)
    
    if not item:
        # 방법 1: HTTPException 직접 사용
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
        # 방법 2: 커스텀 예외 사용 (주석 처리)
        # raise ItemNotFoundError(item_id)
    
    return item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    session: Session = Depends(get_session)
):
    """
    항목을 수정합니다.
    
    에러 처리 패턴:
    - HTTPException은 직접 raise
    - 일반 예외는 핸들러가 처리
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
        # HTTPException은 그대로 전달
        raise
    except Exception as e:
        # 다른 예외는 롤백 후 핸들러가 처리
        session.rollback()
        raise


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    """
    항목을 삭제합니다.
    
    에러 처리 패턴:
    - 명시적인 에러 체크
    - 트랜잭션 롤백
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
# 다양한 에러 상황을 테스트해보세요:
# - 존재하지 않는 항목 조회 (404)
# - 중복된 이름으로 항목 생성 (409)
# - 잘못된 데이터 형식으로 요청 (422)
