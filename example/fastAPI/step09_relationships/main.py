"""
Step 9: 테이블 간 관계 (Relationship)

이 예제에서는 테이블 간 관계를 정의하고 사용하는 방법을 자세히 학습합니다.
- Foreign Key 설정
- Relationship 정의
- 관계를 통한 데이터 접근
- JOIN 쿼리
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import (
    StudentTable, StudentCreate, StudentResponse,
    CollegeTable, CollegeCreate, CollegeResponse
)


app = FastAPI(
    title="FastAPI 학습 예제",
    description="Step 9: 테이블 간 관계 (Relationship)",
    version="1.0.0",
    lifespan=create_db_and_tables
)


# ========== College 엔드포인트 ==========

@app.post("/colleges/", response_model=CollegeResponse, status_code=status.HTTP_201_CREATED)
def create_college(college: CollegeCreate, session: Session = Depends(get_session)):
    """단과대학 생성"""
    try:
        college_orm = CollegeTable.model_validate(college)
        session.add(college_orm)
        session.commit()
        session.refresh(college_orm)
        return college_orm
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"단과대학 생성 중 오류가 발생했습니다: {str(e)}"
        )


@app.get("/colleges/{college_id}", response_model=CollegeResponse)
def get_college(college_id: int, session: Session = Depends(get_session)):
    """단과대학 조회"""
    college = session.get(CollegeTable, college_id)
    if not college:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"College {college_id} not found"
        )
    return college


@app.get("/colleges/", response_model=list[CollegeResponse])
def get_colleges(session: Session = Depends(get_session)):
    """모든 단과대학 조회"""
    statement = select(CollegeTable)
    results = session.exec(statement).all()
    return results


# ========== Student 엔드포인트 ==========

@app.post("/students/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    """
    학생 생성
    
    college_id를 지정하면 해당 단과대학에 소속됩니다.
    """
    try:
        # college_id가 지정된 경우 존재 여부 확인
        if student.college_id:
            college = session.get(CollegeTable, student.college_id)
            if not college:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"College {student.college_id} not found"
                )
        
        student_orm = StudentTable.model_validate(student)
        session.add(student_orm)
        session.commit()
        session.refresh(student_orm)
        return student_orm
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"학생 생성 중 오류가 발생했습니다: {str(e)}"
        )


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, session: Session = Depends(get_session)):
    """학생 조회"""
    student = session.get(StudentTable, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id} not found"
        )
    return student


@app.get("/students/", response_model=list[StudentResponse])
def get_students(session: Session = Depends(get_session)):
    """모든 학생 조회"""
    statement = select(StudentTable)
    results = session.exec(statement).all()
    return results


# ========== Relationship을 사용한 조회 ==========

@app.get("/colleges/{college_id}/students", response_model=list[StudentResponse])
def get_students_by_college(college_id: int, session: Session = Depends(get_session)):
    """
    특정 단과대학에 소속된 학생들을 조회합니다.
    
    Relationship을 사용하여 college.students로 접근할 수 있습니다.
    """
    college = session.get(CollegeTable, college_id)
    if not college:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"College {college_id} not found"
        )
    
    # Relationship을 통해 접근
    # college.students는 해당 단과대학에 소속된 모든 학생 리스트입니다
    return college.students


@app.get("/students/{student_id}/college", response_model=CollegeResponse)
def get_college_by_student(student_id: int, session: Session = Depends(get_session)):
    """
    학생이 소속된 단과대학을 조회합니다.
    
    Relationship을 사용하여 student.college로 접근할 수 있습니다.
    """
    student = session.get(StudentTable, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id} not found"
        )
    
    if not student.college:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id} has no college"
        )
    
    # Relationship을 통해 접근
    return student.college


# ========== JOIN을 사용한 조회 ==========

@app.get("/students-with-college/", response_model=list[dict])
def get_students_with_college(session: Session = Depends(get_session)):
    """
    학생과 소속 단과대학 정보를 함께 조회합니다.
    
    JOIN을 사용하여 한 번의 쿼리로 관련 데이터를 가져옵니다.
    """
    # JOIN 쿼리
    statement = select(StudentTable, CollegeTable).join(
        CollegeTable, StudentTable.college_id == CollegeTable.college_id
    )
    
    results = session.exec(statement).all()
    
    # 결과를 딕셔너리로 변환
    return [
        {
            "student_id": student.student_id,
            "student_name": student.name,
            "student_age": student.age,
            "major": student.major,
            "college_id": college.college_id,
            "college_name": college.college_name,
            "college_tell": college.tell_num
        }
        for student, college in results
    ]


# 실행 방법:
# uvicorn main:app --reload
#
# http://localhost:8000/docs 접속하여 테스트해보세요.
# 1. 먼저 POST /colleges/로 단과대학 생성
# 2. POST /students/로 학생 생성 (college_id 포함)
# 3. GET /colleges/{college_id}/students로 단과대학의 학생 조회
# 4. GET /students/{student_id}/college로 학생의 단과대학 조회
# 5. GET /students-with-college/로 JOIN 쿼리 테스트
