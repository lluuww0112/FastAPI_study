# 04. FastAPI 서버

## 1. 역할

- **REST API** 제공 (Student, College CRUD)
- **PostgreSQL**와 SQLModel(SQLAlchemy)로 연동
- **Nginx** 뒤에서 동작 (포트 8080, 내부 네트워크만)

---

## 2. 디렉터리 구조

```
server/
├── Dockerfile           # 이미지 빌드
├── .env                 # FastAPI/DB 연결용 환경 변수
└── main/
    ├── app.py           # FastAPI 앱, 라우터 등록, root_path
    ├── util.py          # DB 엔진, 세션, 테이블 생성(lifespan)
    ├── requirements.txt
    ├── models/          # SQLModel 모델
    │   ├── __init__.py  # Student, College 노출
    │   ├── Student.py
    │   └── College.py
    └── Routers/
        ├── __init__.py
        ├── get.py
        ├── post.py
        ├── put.py
        └── delete.py
```

---

## 3. Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY server/main/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/main/ ./

EXPOSE 8080

CMD ["gunicorn", "main.app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
```

| 단계 | 설명 |
|------|------|
| `WORKDIR /app` | 컨테이너 내 작업 디렉터리 |
| `COPY server/main/ ./` | `main/` 내용이 `/app`에 복사 → `main/app.py` → `main.app` |
| `EXPOSE 8080` | 이 이미지는 8080을 쓴다고 명시 (실제 노출은 compose에서) |
| **CMD** | **프로덕션**: gunicorn이 uvicorn worker 4개로 `main.app:app` 실행, 8080 바인딩 |

**개발 시**에는 `docker-compose.yml`에서 이 CMD를 덮어써서 `uvicorn app:app --reload`로 실행하고, `./server/main`을 `/app`에 마운트합니다.

---

## 4. app.py: 진입점

```python
from fastapi import FastAPI, Depends
from sqlmodel import Session
import os

from util import create_db_and_tables, get_session
from Routers import post, get, put, delete

mode = os.getenv("MODE", "dev")
root_path = "/main_server" if mode == "dev" else ""

app = FastAPI(
    root_path=root_path,
    title="Project API Docs",
    docs_url="/docs" if mode == "dev" else None,
    lifespan=create_db_and_tables,
)

app.include_router(post.router)
app.include_router(get.router)
app.include_router(put.router)
app.include_router(delete.router)

@app.get("/health")
def health_check(session: Session = Depends(get_session)):
    return {"status": "ok"}
```

| 항목 | 설명 |
|------|------|
| **root_path** | Nginx 앞단 경로. Swagger 등에서 ` /main_server` 아래로 노출 |
| **docs_url** | dev일 때만 `/docs` 활성화, 배포 시 None으로 문서 비노출 |
| **lifespan** | 앱 시작 시 `create_db_and_tables` 실행 → 테이블 생성 |
| **include_router** | get/post/put/delete 라우터 등록 |
| **/health** | 헬스체크용, DB 세션만 주입해서 연결 확인 |

---

## 5. util.py: DB 연결·세션·테이블 생성

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import create_engine, Session, SQLModel
import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_NAME}:{DB_PORT}/{POSTGRES_DB}"
engine = create_engine(POSTGRES_URL, echo=False)

@asynccontextmanager
async def create_db_and_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    # on end (필요 시 정리)

def get_session():
    with Session(engine) as session:
        yield session
```

| 항목 | 설명 |
|------|------|
| **DB_NAME** | Compose 서비스 이름 `postgres` → 컨테이너 간 통신 시 `postgres` 호스트명 |
| **DB_PORT** | `postgresql.conf`의 `port=5000`과 맞춤 (컨테이너 내부 포트) |
| **create_db_and_tables** | lifespan에서 호출. `app.py`에서 `import models` 하므로 여기서 정의한 테이블들이 `SQLModel.metadata`에 등록되고, `create_all`로 생성됨 |
| **get_session** | `Depends(get_session)`으로 라우터에 세션 주입. 요청마다 새 세션, 응답 후 정리 |

---

## 6. 라우터 prefix (실제 경로)

- `Routers/get.py` 등에서 `prefix="/get"`, `prefix="/post"` 등 사용 시:
  - **FastAPI가 받는 경로**: `/get/student`, `/post/student` 등
  - **클라이언트가 호출하는 경로**: `http://localhost/main_server/get/student`, `http://localhost/main_server/post/student`

---

## 7. uvicorn vs gunicorn

| 구분 | uvicorn | gunicorn |
|------|---------|----------|
| 역할 | ASGI 서버. FastAPI(비동기) 실행 | 프로세스/워커 관리 |
| 개발 | `uvicorn app:app --reload` (코드 변경 반영) | 사용 안 함 |
| 프로덕션 | gunicorn의 worker 클래스로 사용 (`uvicorn.workers.UvicornWorker`) | 워커 4개 등으로 다중 프로세스 |

- FastAPI는 **ASGI** 위에서 동작하고, **uvicorn**이 그 ASGI 앱을 실행합니다.
- **gunicorn**은 여러 **uvicorn 워커**를 띄워서 CPU/동시 요청을 나눕니다 (parallelism).
- 개발 시에는 단일 프로세스 uvicorn + `--reload`로 충분합니다.

---

## 8. 환경 변수 (요약)

- **server/.env**, **루트 .env** 에서:
  - `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DB_PORT`, `DB_NAME` → DB 연결
  - `FASTAPI_PORT` → uvicorn 포트 (예: 8080)
  - `MODE` → dev일 때 root_path, docs 활성화

다음 문서에서는 **PostgreSQL** 설정과 healthcheck, 볼륨을 다룹니다.
