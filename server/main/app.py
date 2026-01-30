from fastapi import FastAPI, Depends
from sqlmodel import Session

import os

# /models/__init__.py에 테이블 객체를 임포팅 하는 코드가 추가되어 있기 때문에 models를 임포팅 하면 자동으로 정의해둔 테이블 객체들이 임포팅 됨 
# 이는 테이블을 처음에 초기화 할 때 SQLModel.metadata에 정의한 테이블 객체가 등록하는 것임
from util import create_db_and_tables, get_session

from Routers import post, get, put, delete


mode = os.getenv("MODE", "dev")
root_path = "/main_server" if mode == "dev" else ""

app = FastAPI(
    root_path=root_path,
    title="Project API Docs",
    docs_url="/docs" if mode == "dev" else None, # 배포 환경인 경우 api문서 반환을 끔
    lifespan=create_db_and_tables # 테이블 초기화 함수 설정, 꼭 테이블 생성이 아니더라도 서버가 실행되고 종료될 때 어떤 행동을 취할지 설정할 수 있음
)

# 코드를 작성하다 보면 하나의 서버에 대한 엔드포인트 정의가 과하게 길어질 때가 있음
# 그러한 경우 보다 가독성 높은 개발을 위해 기능 단위를 묶어서 router라는 것을 정의한 다음
# 아래와 같이 .include_router를 하면 됨
# flask의 blueprint와 동일한 기능
app.include_router(post.router)
app.include_router(get.router)
app.include_router(put.router)
app.include_router(delete.router)


@app.get("/health") 
def health_check(session: Session = Depends(get_session)):
    return {"status": "ok"}