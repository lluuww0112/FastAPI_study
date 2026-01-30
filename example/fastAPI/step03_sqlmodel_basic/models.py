"""
Step 3: SQLModel 기본 모델 정의

이 예제에서는 SQLModel을 사용하여 데이터 모델을 정의하는 방법을 학습합니다.
- SQLModel 기본 사용법
- Base, Table, Create, Update 모델 패턴
- 필드 타입 및 제약 조건
"""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


# 1. Base 모델: 공통 필드 정의
# Base 모델은 주로 Not Null 필드들로 구성됩니다
class ItemBase(SQLModel):
    """
    항목의 기본 정보를 담는 모델
    모든 Item 관련 모델의 공통 필드
    """
    name: str  # 필수 필드 (Not Null)
    description: Optional[str] = None  # 선택 필드 (Nullable)


# 2. Table 모델: 데이터베이스 테이블 정의
# table=True를 설정하면 실제 데이터베이스 테이블이 됩니다
class ItemTable(ItemBase, table=True):
    """
    데이터베이스 테이블을 나타내는 모델
    """
    __tablename__ = "items"  # 테이블 이름 지정
    
    # 기본키 설정
    # default=None으로 설정하면 autoincrement가 자동으로 적용됩니다
    item_id: Optional[int] = Field(default=None, primary_key=True)
    
    # 추가 필드들
    price: Optional[float] = Field(default=0.0)  # 기본값 설정
    created_at: datetime = Field(default_factory=datetime.now)  # 함수로 기본값 생성
    
    # unique 제약 조건
    # name: str = Field(unique=True)  # 이름을 unique로 만들고 싶다면


# 3. Create 모델: 데이터 생성 시 사용
# 클라이언트가 보내는 데이터의 구조를 정의합니다
class ItemCreate(ItemBase):
    """
    항목 생성 시 사용하는 모델
    클라이언트가 보내는 데이터 구조
    """
    price: Optional[float] = 0.0


# 4. Update 모델: 데이터 수정 시 사용
# 모든 필드를 Optional로 만들어 부분 업데이트를 가능하게 합니다
class ItemUpdate(SQLModel):
    """
    항목 수정 시 사용하는 모델
    모든 필드가 Optional이므로 필요한 필드만 업데이트 가능
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


# 5. Response 모델: 응답 데이터 구조 정의
# 필요에 따라 응답용 모델을 별도로 정의할 수 있습니다
class ItemResponse(ItemBase):
    """
    항목 조회 시 응답으로 사용하는 모델
    """
    item_id: int
    price: float
    created_at: datetime


# 사용 예시:
# - ItemCreate: POST 요청의 body로 사용
# - ItemTable: 데이터베이스에 저장되는 실제 데이터 구조
# - ItemUpdate: PUT/PATCH 요청의 body로 사용
# - ItemResponse: GET 요청의 응답으로 사용
