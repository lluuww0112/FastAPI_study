"""
Step 9: 테이블 간 관계 (Relationship)

이 예제에서는 SQLModel을 사용하여 테이블 간 관계를 정의하는 방법을 학습합니다.
- Foreign Key 설정
- Relationship 정의
- 관계를 통한 데이터 접근
"""

from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# 순환 참조를 피하기 위해 문자열로 타입 힌트 사용
# CollegeTable은 아래에서 정의되므로 문자열로 참조


class StudentBase(SQLModel):
    """학생의 기본 정보"""
    name: str = Field(unique=True)
    age: int


class StudentTable(StudentBase, table=True):
    """학생 테이블"""
    __tablename__ = "students"
    
    student_id: Optional[int] = Field(default=None, primary_key=True)
    major: Optional[str] = Field(default="미소속")
    
    # Foreign Key: 단과대학 ID 참조
    college_id: Optional[int] = Field(default=None, foreign_key="colleges.college_id")
    
    added_at: datetime = Field(default_factory=datetime.now)
    
    # Relationship: 객체 수준에서 College 객체에 접근 가능
    college: Optional["CollegeTable"] = Relationship(back_populates="students")


class StudentCreate(StudentBase):
    """학생 생성 모델"""
    major: Optional[str] = "미소속"
    college_id: Optional[int] = None


class StudentResponse(StudentBase):
    """학생 응답 모델"""
    student_id: int
    major: Optional[str]
    college_id: Optional[int]
    added_at: datetime


# College 모델 정의
class CollegeBase(SQLModel):
    """단과대학의 기본 정보"""
    college_name: str = Field(unique=True)


class CollegeTable(CollegeBase, table=True):
    """단과대학 테이블"""
    __tablename__ = "colleges"
    
    college_id: Optional[int] = Field(default=None, primary_key=True)
    tell_num: Optional[str] = Field(default=None)
    
    # Relationship: 객체 수준에서 모든 Student 객체에 접근 가능
    students: List["StudentTable"] = Relationship(back_populates="college")


class CollegeCreate(CollegeBase):
    """단과대학 생성 모델"""
    tell_num: Optional[str] = None


class CollegeResponse(CollegeBase):
    """단과대학 응답 모델"""
    college_id: int
    tell_num: Optional[str]
