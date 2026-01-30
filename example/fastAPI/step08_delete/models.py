"""
Step 8: 데이터 삭제 (DELETE)

이 예제에서는 DELETE 요청을 통해 데이터베이스에서 데이터를 삭제하는 방법을 학습합니다.
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


class ItemResponse(ItemBase):
    item_id: int
    price: float
    created_at: datetime
