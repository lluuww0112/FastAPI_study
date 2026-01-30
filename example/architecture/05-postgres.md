# 05. PostgreSQL

## 1. 역할

- **관계형 DB**: Student, College 등 테이블 저장
- **FastAPI**는 SQLModel(PostgreSQL 드라이버: psycopg2)로 접속
- **Docker volume**으로 데이터 영속화

---

## 2. docker-compose에서의 설정

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

| 항목 | 설명 |
|------|------|
| **env_file: .env** | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DB_PORT` 등 |
| **postgresql.conf** | 포트 5000, 타임존, 인코딩, 메모리 등 |
| **postgres_db volume** | 실제 데이터 디렉터리. 재시작/재생성해도 데이터 유지 |
| **5001:5000** | 호스트 5001 → 컨테이너 5000. DBeaver 등은 `localhost:5001`로 접속 |
| **healthcheck** | FastAPI는 `depends_on: postgres, condition: service_healthy`로 이게 통과할 때까지 대기 |
| **command** | 기본 설정 대신 우리가 준 `postgresql.conf` 사용 |

---

## 3. postgresql.conf 요약

```ini
# 접속
listen_addresses = '*'
port = 5000

# 시간
timezone = 'Asia/Seoul'
log_timezone = 'Asia/Seoul'
datestyle = 'iso, ymd'

# 인코딩 (한글 등)
client_encoding = 'utf8'
default_text_search_config = 'pg_catalog.simple'

# 메모리/연결
shared_buffers = 512MB
max_connections = 50

# 로깅 (개발 시)
log_statement = 'all'
```

- **port=5000**: 컨테이너 내부 포트. FastAPI의 `DB_PORT`와 동일해야 함.
- **listen_addresses='*'**: Compose 네트워크 안의 다른 컨테이너(fastapi)에서 접속 가능.
- **client_encoding='utf8'**: 한글 등 UTF-8 안전하게 사용.

---

## 4. FastAPI와의 연결

**util.py**에서:

```text
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_NAME}:{DB_PORT}/{POSTGRES_DB}"
```

- **DB_NAME**: Compose 서비스 이름 `postgres` → 컨테이너 이름으로 해석됨.
- **DB_PORT**: 컨테이너 **내부** 포트 `5000` (postgresql.conf의 `port=5000`).
- 호스트에서 접속할 때만 `localhost:5001`(호스트 포트) 사용.

---

## 5. healthcheck

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -p ${DB_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
  interval: 5s
  timeout: 5s
  retries: 5
  start_period: 10s
```

- **pg_isready**: 해당 포트/유저/DB로 접속 가능한지 확인.
- **start_period: 10s**: 기동 직후 10초는 실패해도 unhealthy로 치지 않음.
- **condition: service_healthy**인 FastAPI는 이 검사가 성공한 뒤에만 시작합니다.

---

## 6. 데이터 영속성 (볼륨)

```yaml
volumes:
  - postgres_db:/var/lib/postgresql
```

- 데이터 디렉터리를 **named volume**에 두어, 컨테이너를 지워도 데이터가 남습니다.
- `docker compose down -v` 시 `postgres_db`까지 삭제되므로, 데이터를 지우고 싶을 때만 `-v` 사용.

---

## 7. DBeaver 등에서 접속

| 항목 | 값 |
|------|-----|
| Host | localhost |
| Port | **5001** (호스트에 매핑된 포트) |
| Database | `.env`의 `POSTGRES_DB` |
| User | `POSTGRES_USER` |
| Password | `POSTGRES_PASSWORD` |

다음 문서에서는 **요청/응답이 어떻게 흐르는지(데이터 플로우)**를 정리합니다.
