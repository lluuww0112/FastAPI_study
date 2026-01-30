from pydantic import BaseModel, Field
from typing import Annotated

from fastapi import APIRouter
from fastapi import Path, Query
from fastapi import HTTPException, status
from fastapi import Depends

from sqlmodel import Session
from sqlmodel import select

from util import get_session
from models import Student, College




router = APIRouter(
    prefix="/get",
    tags=["Get Api"], # api 문서 자동화시 사용할 tag, 각 api가 어느 라우터에 해당하는지 알 수 있음
    responses={404 : {"description" : "Not Found"}} # 라우터로 요청을 넘기고 404코드가 반환될 때 클라이언트로 전달할 데이터를 설정
)



# COLLEGE ------------------------------------------------------------------------------------------------------------------------------------------------------------

class Query_get_college(BaseModel):
    offset : int | None = Field(default=0, ge=0, description="조회를 시작할 첫 위치")
    limit : int | None = Field(default=10, ge=1, description="조회 범위")


@router.get('/college', response_model=list[College.CollegeTable], description="단과대 정보 조회 API")
def get_college_by_range(
    q : Annotated[Query_get_college, Query(description="범위 조회를 위한 쿼리입니다")],
    session : Session = Depends(get_session)
):
    
    try:
        sql_query = (
            select(College.CollegeTable)
            .offset(q.offset)
            .limit(q.limit)
        )
        
        results = session.exec(sql_query).all()
        if not len(results): # 조회된 결과가 없는 경우
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="조회된 데이터가 없습니다")

        return results

    except HTTPException:
        raise
    except Exception as e:
        print(f">>>>> Error Messege <<<<< \n {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="조회를 하는 도중 오류가 발생했습니다"
        )


@router.get('/college/{college_id}', response_model=College.CollegeTable)
def get_college_by_collge_id(
    college_id : Annotated[int, Path(description="특정 단과대 정보를 조회하는 경우 사용되는 정수")],
    session : Session = Depends(get_session)
):
    
    try:
        sql_query = (
            select(College.CollegeTable)
            .where(College.CollegeTable.college_id == college_id)
        )    
        
        result = session.exec(sql_query).one_or_none()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="조회된 데이터가 없습니다")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="단과대학을 조회하는 도중 오류가 발생했습니다"
        )



# STUDENT ------------------------------------------------------------------------------------------------------------------------------------------------------------


class Query_get_student_by_arage(BaseModel):
    offset : int | None = Field(default=0, ge=0, description="학생 범위 조회를 위한 offset")
    limit : int | None = Field(default=10, ge=1, description="학생 범위 조회를 위한 limit")


@router.get("/student", response_model=list[Student.StudentTable])
async def get_student_by_arange(
    q : Annotated[Query_get_student_by_arage, Query(description="학생 범위 조회를 위한 쿼리")],
    session : Session = Depends(get_session)
):
    
    try:
        sql_query = (
            select(Student.StudentTable)
            .offset(q.offset)
            .limit(q.limit)
        )

        results = session.exec(sql_query).all()

        if not len(results):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="조회된 데이터가 없습니다")
        
        return results
    
    except HTTPException:
        raise
    except Exception as e:
        print(f">>>>>>> Error Message <<<<<<<< \n {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="학생 데이터를 조회하는 도중 오류가 발생했습니다"
        )



@router.get("/student/{student_id}")
def get_student_by_student_id(
    student_id : Annotated[str, Path(description="student_id로 단일 조회하기 위한 파라미터입니다")],
    session : Session = Depends(get_session)
):
    try:

        sql_query = (
            select(Student.StudentTable)
            .where(Student.StudentTable.student_id == student_id)
        )

        result = session.exec(sql_query).one_or_none()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="조회된 데이터가 없습니다")
        
        return result

    except HTTPException:
        raise
    except Exception as e:
        print(f">>>> Error message <<<< \n {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="학생 데이터를 조회하는 도중 오류가 발생헀습니다"
        )
    