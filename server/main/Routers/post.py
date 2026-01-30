from enum import Enum
from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi import Path, Query, Body
from fastapi import HTTPException, status
from sqlmodel import Session

from util import get_session
from models import Student, College # models에 정의된 객체들을 가져옴


router = APIRouter(
    prefix="/post",
    tags=["Post Api"], # api 문서 자동화시 사용할 tag, 각 api가 어느 라우터에 해당하는지 알 수 있음
    responses={404 : {"description" : "Not Found"}} # 라우터로 요청을 넘기고 404코드가 반환될 때 클라이언트로 전달할 데이터를 설정
)


@router.post('/college', response_model=College.CollegeTable)
async def post_college(
    college : Annotated[College.CollegeCreate, Body(description="단과대 포스팅을 위한 요청바디입니다")],
    session : Session = Depends(get_session)
):
    
    try:
        college_orm = College.CollegeTable.model_validate(college) # 요청 body를 이용해서 orm객체를 생성

        session.add(college_orm) # db 버퍼상에 college_orm을 추가
        session.commit() # 실제 db상에 반영
        session.refresh(college_orm) # db에 넣는 도중에 새롭게 추가된 id 등의 칼럼을 college_orm에 동기화

        return college_orm

    except Exception as e:
        # session을 통해 db에 작업들을 하기 전으로 복귀, 개발하다보면 특정 비지니즈 로직을 위해 복수의 테이블을 건드려야 할 때가 있음
        # 이 때 A 테이블은 잘 건드렸다가 B테이블은 잘못건드려서 오류가 발생했다면 안전성을 위해 A테이블에 작업한 내용도 없던일이 되어야 함
        # 따라서 rollback 메소드는 이를 편리하게 관리하도록 해줌
        session.rollback() 

        print(f"error message \n {str(e)}")
    
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Colleges table에 데이터를 추가하는 도중 오류가 발생했습니다"
        )
    


@router.post('/student', response_model=Student.StudentTable)
async def post_student(
    student : Annotated[Student.StudentCreate, Body(description="학생 포스팅을 위한 요청 바디입니다")],
    session : Session = Depends(get_session)
):
    
    try:
        student_orm = Student.StudentTable.model_validate(student)

        session.add(student_orm)
        session.commit()
        session.refresh(student_orm)

        return student_orm

    except Exception as e:
        session.rollback()
        print(f"error message \n {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Students table에 데이터를 추가하는 도중 오류가 발생했습니다"
        )
    