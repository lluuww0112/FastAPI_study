from datetime import datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


# Optional[type] = None 을 하면 nullable
# type = ~ 를 하면 not null
# 이 때 nullable 여부 말고도 여러 제약 조건을 설정하고 싶을 때는 Filed를 사용
# 기본적으로 각 속성의 데이터 타입은 파이썬에서 지원하는 데이터 타입으로 설정하면 자동으로 DB상에 알맞는 데이터 타입으로 지정해줌


if TYPE_CHECKING:
    from College import CollegeTable


class StudentBase(SQLModel): # 각 객체를 정의하는 최소한의 필수 정보만으로 구성, 주로 Not Null값이 위치함
    name : str = Field(unique=True) # 이름은 중복되지 않도록 unique설정을 가함
    age : int


class StudentTable(StudentBase, table=True):
    __tablename__ = "Students"
    student_id : Optional[int] = Field(default=None, primary_key=True) # 기본키 지정됨, 이 때 default=None에 int이기 때문에 autoincrement 제약조건 적용됨
    major : Optional[str] = Field(default="미소속") # 여거서 nullable 이지만 default값이 있다는 건 db에 데이터를 넣기 위해 객체를 생성할 때 None이 들어오면 자동으로 default값으로 채우고 나중에 서비스 돌아가다가 해당 값이 None으로 변경될 수 있다는 것
    college_id : Optional[int] = Field(default=None, foreign_key="Colleges.college_id")
    added_at : datetime = Field(default_factory=datetime.now) # default값을 함수로 생성해야 하는 경우 default_factory로 함수를 연결, 이 때 default value 생성 함수가 인자가 필요하다면 lambda식을 사용하면 됨

    collge : Optional["CollegeTable"] = Relationship(back_populates="students") # 객체 수준에서 Student와 연관된 College 객체를 바로 접근 가능해짐


class StudentCreate(StudentBase):
    major : Optional[str] = "미소속"
    college_id : Optional[int] = None


class StudentUpdate(StudentBase):
    name : str | None = None
    age : int | None = None
    major : str | None = None
    collge_id : int | None = None
    