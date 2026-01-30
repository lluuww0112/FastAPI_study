"""
Step 7: 데이터 수정 (PUT)

이 예제에서는 PUT 요청을 통해 데이터베이스의 데이터를 수정하는 방법을 학습합니다.
"""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class ItemBase(SQLModel):
    name: str
    description: Optional[str] = None


class ItemTable(ItemBase, table=True):
    __tablename__ = "items"
    
    item_id: Optional[int] = Field(default=None, primary_key=True)
    price: Optional[float] = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.now)


class ItemCreate(ItemBase):
    price: Optional[float] = 0.0


class ItemUpdate(SQLModel):
    """수정할 필드만 Optional로 정의"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ItemResponse(ItemBase):
    item_id: int
    price: float
    created_at: datetime
