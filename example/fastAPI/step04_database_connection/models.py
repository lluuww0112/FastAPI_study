"""
Step 4: 데이터베이스 연결 및 세션 관리

이 예제에서는 SQLModel을 사용하여 데이터베이스에 연결하고 세션을 관리하는 방법을 학습합니다.
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
