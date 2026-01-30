from typing import Annotated
from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Path, Query
from fastapi import HTTPException, status
from fastapi import Depends

from sqlmodel import Session, select

from models import Student, College
from util import get_session



router = APIRouter(
    prefix="/delete",
    tags=["Delete Api"], # api 문서 자동화시 사용할 tag, 각 api가 어느 라우터에 해당하는지 알 수 있음
    responses={404 : {"description" : "Not Found"}} # 라우터로 요청을 넘기고 404코드가 반환될 때 클라이언트로 전달할 데이터를 설정
)



@router.delete("/college/{college_id}")
async def delete_collge_by_college_id(
    college_id : Annotated[int, Path(description="삭제할 단과대학을 지정할 id입니다")],
    session : Session = Depends(get_session)
):
    try:
        college_orm = session.get(College.CollegeTable, college_id)
        if not college_orm: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 단과대입니다")

        session.delete(college_orm)
        session.commit()

        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="단과대가 삭제되었습니다")
    
    except HTTPException:
        session.rollback() 
        raise
    except Exception as e:
        session.rollback()        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="단과 대학을 삭제하는 도중 오류가 발생했습니다"
        )



@router.delete("/student/{student_id}")
async def delete_student_by_student_ud(
    student_id : Annotated[int, Path(description="삭제할 학생을 지정할 id입니다")],
    session : Session = Depends(get_session)
):
    try:
        
        student_orm = session.get(Student.StudentTable, student_id)
        if not student_orm: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 학생입니다")

        student_name = student_orm.name
        session.delete(student_orm)
        session.commit()

        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"{student_name} 학생이 삭제되었습니다")

    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="학생 정보를 삭제하는 도중 오류가 발생했습니다"
        )