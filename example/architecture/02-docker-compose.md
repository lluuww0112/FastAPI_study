# 02. Docker Compose

## 1. Docker Compose란?

**Docker Compose**는 여러 컨테이너를 하나의 “프로젝트”로 정의하고, 한 번에 실행·중지할 수 있게 해주는 도구입니다.

- **단일 YAML 파일** (`docker-compose.yml`)로 서비스, 네트워크, 볼륨을 정의
- `docker compose up` 한 번으로 **nginx + fastapi + postgres** 모두 기동
- 서비스 간 **의존성**(`depends_on`)과 **healthcheck**로 **시작 순서** 제어

---

## 2. 이 프로젝트의 docker-compose.yml 구조

```yaml
services:
  nginx:      # 리버스 프록시
  fastapi:    # API 서버
  postgres:   # 데이터베이스

volumes:
  postgres_db:   # DB 데이터 영속화
```

---

## 3. 서비스별 설정 해설

### 3.1 Nginx

```yaml
nginx:
  image: nginx:latest
  container_name: nginx
  ports:
    - 80:80
  volumes:
    - "./nginx/nginx.conf:/etc/nginx/nginx.conf"
  depends_on:
    - fastapi
  restart: always
```

| 항목 | 의미 |
|------|------|
| `image` | 공식 nginx 이미지 사용 |
| `ports: 80:80` | 호스트 80 → 컨테이너 80 (클라이언트 접속 포트) |
| `volumes` | 로컬 `nginx.conf`로 설정 덮어쓰기 |
| `depends_on: fastapi` | fastapi 컨테이너가 먼저 떠 있도록 함 |
| `restart: always` | 컨테이너가 죽으면 자동 재시작 |

---

### 3.2 FastAPI

```yaml
fastapi:
  container_name: fastapi
  build:
    context: .
    dockerfile: server/Dockerfile
  env_file:
    - ./server/.env
    - ./.env
  volumes:
    - ./server/main:/app
  depends_on:
    postgres:
      condition: service_healthy
  command: uvicorn app:app --host 0.0.0.0 --port ${FASTAPI_PORT} --reload
  restart: always
```

| 항목 | 의미 |
|------|------|
| `build` | 프로젝트 루트(`.`)를 context로, `server/Dockerfile`로 이미지 빌드 |
| `env_file` | `server/.env` + 루트 `.env` (나중 것이 같은 변수 덮어씀) |
| **`volumes: ./server/main:/app`** | **개발 시** 호스트의 `server/main`을 컨테이너 `/app`에 마운트 → 코드 수정 시 재빌드 없이 반영 |
| **`depends_on.postgres.condition: service_healthy`** | Postgres가 **healthcheck 통과**한 뒤에만 FastAPI 시작 |
| **`command`** | Dockerfile의 `CMD` 대신 **uvicorn + --reload**로 실행 (개발용). 새 패키지 추가 시에는 이미지 재빌드 필요 |

**개발 vs 프로덕션**

- **개발**: `volumes` + `command`(uvicorn --reload) → 소스 변경만 하면 반영
- **프로덕션**: `volumes`·`command` 제거하고 Dockerfile의 `CMD`(gunicorn + uvicorn worker) 사용

---

### 3.3 Postgres

```yaml
postgres:
  image: postgres:18
  container_name: postgres
  env_file:
    - ".env"
  volumes:
    - ./db/postgresql.conf:/etc/postgresql/postgresql.conf
    - postgres_db:/var/lib/postgresql
  ports:
    - 5001:5000
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -p ${DB_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
    interval: 5s
    timeout: 5s
    retries: 5
    start_period: 10s
  command: postgres -c config_file=/etc/postgresql/postgresql.conf
  restart: always
```

| 항목 | 의미 |
|------|------|
| `volumes` | 설정 파일 주입 + **named volume** `postgres_db`로 데이터 디렉터리 영속화 |
| `ports: 5001:5000` | 호스트 5001 → 컨테이너 5000 (DBeaver 등에서 `localhost:5001`로 접속) |
| **healthcheck** | `pg_isready`로 DB 준비 여부 확인. FastAPI는 이게 성공할 때까지 대기 |
| **command** | 커스텀 `postgresql.conf`로 Postgres 기동 (포트 5000 등) |

---

## 4. 볼륨 (Volumes)

```yaml
volumes:
  postgres_db:
```

- **Named volume** `postgres_db`: Docker가 관리하는 경로에 DB 데이터 저장
- `docker compose down -v` 하면 이 볼륨까지 삭제되므로, 데이터 보존이 필요하면 `-v` 없이 down

**왜 로컬 디렉터리(`./db/...`)가 아니라 named volume?**

- 성능, 권한, 백업 등 volume 기능을 Docker가 제공
- DB 데이터는 보통 `postgres_db` 같은 전용 볼륨에 두는 패턴 사용

---

## 5. 네트워크

Compose는 **기본 네트워크**를 하나 만들고, 모든 서비스를 그 안에 넣습니다.

- **서비스 이름 = 호스트명**
  - FastAPI에서 DB 접속: `DB_NAME=postgres`, `DB_PORT=5000` (컨테이너 내부 포트)
  - Nginx에서 FastAPI 호출: `http://fastapi:8080`

---

## 6. 의존성과 시작 순서

```
postgres (healthcheck 통과)
    ↓
fastapi (depends_on: postgres, condition: service_healthy)
    ↓
nginx (depends_on: fastapi)
```

- Postgres가 **healthy** 된 후에 FastAPI가 시작하고, FastAPI가 뜬 다음 Nginx가 동작합니다.
- Nginx는 FastAPI만 의존하므로, FastAPI가 떠 있으면 기동합니다.

---

## 7. 자주 쓰는 명령어

```bash
# 전체 기동 (백그라운드)
docker compose up -d

# 로그 보기
docker compose logs -f

# 특정 서비스만 재시작
docker compose restart fastapi

# 전체 중지 + 볼륨까지 삭제 (DB 데이터 삭제됨)
docker compose down -v

# 이미지까지 다시 빌드해서 기동
docker compose up -d --build
```

다음 문서에서는 **Nginx** 설정(리버스 프록시, upstream, location)을 다룹니다.
