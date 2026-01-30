from datetime import datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


# Optional[type] = None 을 하면 nullable
# type = ~ 를 하면 not null
# 이 때 nullable 여부 말고도 여러 제약 조건을 설정하고 싶을 때는 Filed를 사용
# 기본적으로 각 속성의 데이터 타입은 파이썬에서 지원하는 데이터 타입으로 설정하면 자동으로 DB상에 알맞는 데이터 타입으로 지정해줌


if TYPE_CHECKING:
    from Student import StudentTable



class CollgeBase(SQLModel): # 요청, 응답, 테이블 구조 등등을 정의하기 위한 Base가 되는 필드를 정의
    college_name : str = Field(unique=True)


class CollegeTable(CollgeBase, table=True): # DB 수준에서 관리해야 하는 것들이 Table 객체에서 정의
    __tablename__ = "Colleges"
    
    college_id : Optional[int] = Field(default=None, primary_key=True) # autoincrement
    tell_num : Optional[str] = Field(default=None)

    students : List["StudentTable"] = Relationship(back_populates="collge") # 객체 수준에서 Collge와 연결된 모든 Student 객체를 리스트 형태로 접근 가능해짐
    

class CollegeCreate(CollgeBase):
    tell_num : Optional[str] = None


class CollgeUpdate(CollgeBase):
    college_name : str | None = None
    tell_num : str | None = None