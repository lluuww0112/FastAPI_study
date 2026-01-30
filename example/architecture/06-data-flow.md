# 06. 데이터 플로우 (요청/응답 흐름)

## 1. 전체 흐름

```
[클라이언트]
    │  GET http://localhost/main_server/get/student
    ▼
[Nginx :80]
    │  rewrite: /main_server/get/student → /get/student
    │  proxy_pass → http://fastapi:8080/get/student
    ▼
[FastAPI :8080]
    │  Routers/get.py → DB 조회
    │  get_session() → Session(engine)
    ▼
[PostgreSQL :5000]
    │  SELECT ... FROM "Students" ...
    ▼
[FastAPI] ← 결과
    │  JSON 응답
    ▼
[Nginx] ← 응답
    │  그대로 클라이언트로 전달
    ▼
[클라이언트] ← JSON
```

---

## 2. 포트·경로 매핑 정리

| 구간 | 주체 | 주소/경로 |
|------|------|-----------|
| 클라이언트 → Nginx | 브라우저/앱 | `http://localhost/main_server/...` (호스트 80) |
| Nginx → FastAPI | Nginx | `http://fastapi:8080/...` (경로: `/main_server` 제거 후) |
| FastAPI → PostgreSQL | FastAPI(util.py) | `postgres:5000` (컨테이너 내부) |
| 호스트 → PostgreSQL (DBeaver 등) | 개발자 PC | `localhost:5001` → 컨테이너 5000 |

---

## 3. 예시: 학생 목록 조회

**1. 클라이언트 요청**

```http
GET http://localhost/main_server/get/student?offset=0&limit=10
Host: localhost
```

**2. Nginx**

- `location /main_server/` 매칭
- `rewrite ^/main_server(.*)$ $1 break` → 경로는 `/get/student`
- `proxy_pass http://main_server` → `http://fastapi:8080/get/student?offset=0&limit=10`

**3. FastAPI**

- `Routers/get.py`의 `get_student_by_arange` 등에서 `Query`로 offset, limit 파싱
- `Depends(get_session)`으로 세션 획득
- `select(Student.StudentTable).offset().limit()` 실행

**4. PostgreSQL**

- `postgres:5000`으로 연결 (util.py의 `POSTGRES_URL`)
- SQL 실행 후 결과 반환

**5. 응답**

- FastAPI → JSON 리스트
- Nginx → 그대로 클라이언트에 전달

---

## 4. 환경 변수로 보는 연결 정보

| 변수 | 사용처 | 의미 |
|------|--------|------|
| (호스트 80) | 클라이언트 | Nginx 접속 포트 |
| FASTAPI_PORT=8080 | FastAPI 컨테이너 | uvicorn 리스닝 포트. Nginx가 `fastapi:8080`으로 접근 |
| DB_NAME=postgres | util.py | PostgreSQL 호스트명 (서비스 이름) |
| DB_PORT=5000 | util.py | PostgreSQL **컨테이너 내부** 포트 |
| 5001:5000 | docker-compose | 호스트 5001 → postgres 5000 (DBeaver용) |

---

## 5. 다이어그램 (요약)

```
                    호스트
┌────────────────────────────────────────────────────────┐
│  localhost:80          localhost:5001 (선택)            │
│       │                         │                      │
│  ┌────▼────┐              ┌─────▼─────┐                │
│  │  Nginx  │              │ DBeaver 등 │               │
│  │  :80    │              │ (DB 직접)  │                │
│  └────┬────┘              └─────┬─────┘                │
│       │                          │                     │
│       │  /main_server/*          │                     │
│       ▼                          ▼                     │
│  ┌─────────────┐           ┌─────────────┐             │
│  │   FastAPI   │──────────►│  PostgreSQL │             │
│  │   :8080     │  postgres │   :5000     │             │
│  └─────────────┘  :5000    └─────────────┘             │
│                                                        │
│              Docker Compose Network                    │
└────────────────────────────────────────────────────────┘
```

다음 문서에서는 **개발 환경 vs 프로덕션 환경** 차이를 정리합니다.
