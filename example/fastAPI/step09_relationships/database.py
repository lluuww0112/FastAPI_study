"""
데이터베이스 연결 및 세션 관리
"""

from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session, SQLModel
import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "testdb")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

engine = create_engine(POSTGRES_URL, echo=True)


@asynccontextmanager
async def create_db_and_tables(app):
    print("데이터베이스 테이블을 생성합니다...")
    # models를 import하여 테이블이 등록되도록 함
    from models import StudentTable, CollegeTable
    SQLModel.metadata.create_all(engine)
    print("테이블 생성 완료!")
    yield
    print("서버를 종료합니다...")


def get_session():
    with Session(engine) as session:
        yield session
