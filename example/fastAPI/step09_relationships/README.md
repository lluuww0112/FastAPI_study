# Step 9: 테이블 간 관계 (Relationship)

## 학습 목표
- Foreign Key 설정 방법
- Relationship 정의 및 사용
- 관계를 통한 데이터 접근
- JOIN 쿼리 사용법
- 순환 참조 문제 해결 (TYPE_CHECKING)

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 테스트 방법

1. 단과대학 생성:
   ```bash
   POST /colleges/
   {
     "college_name": "공과대학",
     "tell_num": "02-1234-5678"
   }
   ```

2. 학생 생성 (단과대학 소속):
   ```bash
   POST /students/
   {
     "name": "홍길동",
     "age": 20,
     "major": "컴퓨터공학과",
     "college_id": 1
   }
   ```

3. 관계를 통한 조회:
   - GET /colleges/1/students (단과대학의 학생들)
   - GET /students/1/college (학생의 단과대학)
   - GET /students-with-college/ (JOIN 쿼리)

## 주요 개념

### Foreign Key

```python
college_id: Optional[int] = Field(
    default=None, 
    foreign_key="colleges.college_id"
)
```

- 다른 테이블의 기본키를 참조
- 데이터베이스 수준의 제약 조건
- 참조 무결성 보장

### Relationship

```python
# Student에서 College 접근
college: Optional["CollegeTable"] = Relationship(
    back_populates="students"
)

# College에서 Student 접근
students: List["StudentTable"] = Relationship(
    back_populates="college"
)
```

- 객체 수준에서 관계된 데이터 접근
- `back_populates`: 양방향 관계 설정
- 자동으로 JOIN 쿼리 생성

### 순환 참조 해결

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import CollegeTable
```

- `TYPE_CHECKING`: 타입 체크 시에만 import
- 런타임에는 순환 참조 문제 없음

### 관계 접근

```python
# Student에서 College 접근
student.college  # CollegeTable 객체

# College에서 Student 접근
college.students  # List[StudentTable]
```

### JOIN 쿼리

```python
statement = select(StudentTable, CollegeTable).join(
    CollegeTable, 
    StudentTable.college_id == CollegeTable.college_id
)
```

- 여러 테이블을 한 번에 조회
- 성능 최적화

## 관계 종류

1. **일대다 (One-to-Many)**: College → Students
   - 하나의 단과대학에 여러 학생
   - Foreign Key는 "다" 쪽에 위치

2. **다대일 (Many-to-One)**: Students → College
   - 여러 학생이 하나의 단과대학에 소속
   - Foreign Key로 표현

## 주의사항

1. **Foreign Key 제약 조건**: 존재하지 않는 ID를 참조하면 오류 발생
2. **CASCADE 삭제**: 부모 삭제 시 자식도 삭제할지 설정 필요
3. **순환 참조**: TYPE_CHECKING을 사용하여 해결
4. **성능**: Relationship은 자동으로 JOIN하지만, 필요시 명시적 JOIN 사용

## 다음 단계

이제 테이블 간 관계를 배웠으니, Step 10에서 에러 처리 및 예외 처리를 학습합니다.
