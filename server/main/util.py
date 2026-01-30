from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import create_engine, Session, SQLModel

import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 형식: postgresql://사용자이름:비밀번호@호스트:포트/데이터베이스이름
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_NAME}:{DB_PORT}/{POSTGRES_DB}"


engine = create_engine(POSTGRES_URL, echo=False) # echo를 끄면 db엔진의 로그 출력이 보이지 않음

# 다음 함수를 fastapi app객체의 lifespan으로 설정하면 DB에 테이블이 존재하지 않을 때 미리 정의해둔 모든 테이블을 생성함
# SQLModel.metadata로 테이블을 생성하려면 미리 생성할 모든 테이블 객체가 코드 상으로 임포팅되어 있어야 함
# 이 때 /models/__init__.py에 생성할 테이블에 해당하는 객체를 임포팅 해놓고 app.py에서 import models를 하는게 편리하게 테이블을 초기화 하는 방법임
# create_all은 테이블이 없을 때만 생성해주기 떄문에 기존 테이블들의 구조가 바뀐다거나 하면 Alembic같은 툴을 사용해야 함
# 아래와 같이 비동기컨텍스트매니저를 사용하면 서버가 실행되고 종료될 때 어떤 행동을 취할지 설정 가능
# 예를 들어 예기치 않은 오류로 서버가 종료된 경우 오류가 발생하기 전 작업하던 내용들을 따로 저장해 뒀다가 다시 실행될 때 내용을 불러올 수 있음
@asynccontextmanager
async def create_db_and_tables(app : FastAPI):
    # on start action
    SQLModel.metadata.create_all(engine)
    
    yield # 서버가 정상적으로 동작하기 시작하면 yield를 통해 craete_db_and_tables함수를 빠져 나가 다른 코드를 실행함, 다른 코드들이 모두 종료 되면 yield 아래 내용을 실행

    # on end action
    # ~


# 편하게 세션을 가져오기 위한 함수 어떻게 사용되는지 확인하려면 app.py를 보면 바로 알 수 있음
def get_session():
    with Session(engine) as session:
        yield session