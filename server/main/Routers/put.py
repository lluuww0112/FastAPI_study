from typing import Annotated
from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path, Body
from fastapi import HTTPException, status

from sqlmodel import Session, select

from models import Student, College
from util import get_session




router = APIRouter(
    prefix="/put",
    tags=["Put Api"], # api 문서 자동화시 사용할 tag, 각 api가 어느 라우터에 해당하는지 알 수 있음
    responses={404 : {"description" : "Not Found"}} # 라우터로 요청을 넘기고 404코드가 반환될 때 클라이언트로 전달할 데이터를 설정
)




@router.put("/college/{college_id}")
def put_college_by_id(
    college_id : Annotated[int, Path(description="수정할 단과대학을 지정하기 위한 경로 파라미터")],
    college_data : Annotated[College.CollgeUpdate , Body(description="단과대학 데이터를 수정하기 위한 요청 바디")],
    session : Session = Depends(get_session)
):
    try:
        
        college_orm = session.get(College.CollegeTable, college_id)
        if not college_orm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 단과대학 입니다")

        # 클라이언트가 전달한 데이터만 update
        # 즉 exclude_unset을 통해 None이 아닌 값만 update하게 됨
        update_date = college_data.model_dump(exclude_unset=True)
        for key, value in update_date.items():
            setattr(college_orm, key, value)
        
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="단과대학 정보가 수정되었습니다")
        
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="단과대학 정보 수정 도중 오류 발생"
        )
    


@router.put("/student/{student_id}")
def put_studet_by_student_id(
    student_id : Annotated[str, Path(description="수정할 학생을 지정하기 위한 경로 파라미터")],
    student_data : Annotated[Student.StudentUpdate, Body(description="수정할 학생 정보")],
    session : Session = Depends(get_session)
):
    try:

        student_orm = session.get(Student.StudentTable, student_id)
        if not student_orm: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 학생입니다")

        update_data = student_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(student_orm, key, value)
        
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="학생 정보가 수정되었습니다")
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="학생 정보를 수정하는 도중 오류가 발생했습니다"
        )