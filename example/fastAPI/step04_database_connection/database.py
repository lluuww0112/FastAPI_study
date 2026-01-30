"""
데이터베이스 연결 및 세션 관리

이 파일에서는 데이터베이스 엔진 생성과 세션 관리를 담당합니다.
"""

from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session, SQLModel
import os

# 환경 변수에서 데이터베이스 연결 정보 가져오기
# 실제 사용 시 .env 파일을 사용하는 것을 권장합니다
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "testdb")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# PostgreSQL 연결 URL 형식: postgresql://사용자이름:비밀번호@호스트:포트/데이터베이스이름
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

# SQLite를 사용하는 경우 (학습용으로 더 간단함)
# SQLITE_URL = "sqlite:///./example.db"
# engine = create_engine(SQLITE_URL, echo=True)

# 데이터베이스 엔진 생성
# echo=True로 설정하면 SQL 쿼리가 콘솔에 출력됩니다 (디버깅용)
engine = create_engine(POSTGRES_URL, echo=True)


# 서버 시작 시 테이블 생성하는 함수
# FastAPI의 lifespan에 등록하여 서버 시작 시 자동 실행됩니다
@asynccontextmanager
async def create_db_and_tables(app):
    """
    서버 시작 시 데이터베이스 테이블을 생성합니다.
    
    주의: SQLModel.metadata.create_all()은 테이블이 없을 때만 생성합니다.
    기존 테이블의 구조를 변경하려면 Alembic 같은 마이그레이션 도구를 사용해야 합니다.
    """
    # 서버 시작 시 실행되는 코드
    print("데이터베이스 테이블을 생성합니다...")
    SQLModel.metadata.create_all(engine)
    print("테이블 생성 완료!")
    
    yield  # 서버가 실행되는 동안 여기서 대기
    
    # 서버 종료 시 실행되는 코드 (필요한 경우)
    print("서버를 종료합니다...")


# 세션을 가져오는 함수
# FastAPI의 Depends를 사용하여 의존성 주입으로 세션을 받을 수 있습니다
def get_session():
    """
    데이터베이스 세션을 생성하고 반환합니다.
    
    사용법:
        @app.get("/items/")
        def get_items(session: Session = Depends(get_session)):
            # 세션 사용
            pass
    
    with 문을 사용하여 자동으로 세션이 닫히도록 합니다.
    """
    with Session(engine) as session:
        yield session
