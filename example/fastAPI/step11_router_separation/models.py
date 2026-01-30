"""
Step 11: 라우터 분리 및 구조화

이 예제에서는 라우터를 별도 파일로 분리하여 코드를 구조화하는 방법을 학습합니다.
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
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ItemResponse(ItemBase):
    item_id: int
    price: float
    created_at: datetime
