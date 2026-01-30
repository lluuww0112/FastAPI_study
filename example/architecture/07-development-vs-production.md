# 07. 개발 환경 vs 프로덕션 환경

## 1. 개요

이 프로젝트는 **개발** 시에는 `docker-compose.yml`의 `volumes`와 `command`로 “코드 변경만 하면 반영”되도록 하고, **프로덕션**에서는 Dockerfile의 `CMD`(gunicorn + uvicorn worker)와 이미지 빌드로 고정된 코드를 서빙하는 구조입니다.

---

## 2. 개발 환경 (현재 docker-compose.yml)

| 항목 | 설정 | 목적 |
|------|------|------|
| **FastAPI volumes** | `./server/main:/app` | 호스트 코드를 컨테이너에 실시간 반영 |
| **FastAPI command** | `uvicorn app:app --host 0.0.0.0 --port ${FASTAPI_PORT} --reload` | 코드 변경 시 자동 재시작 |
| **Postgres ports** | `5001:5000` | DBeaver 등에서 `localhost:5001`로 DB 접속 |
| **docs_url** | `/docs` 활성화 | Swagger UI로 API 테스트 |
| **root_path** | `/main_server` | Nginx 앞단 경로와 문서 URL 맞춤 |

**특징**

- `server/main` 아래 파일을 수정하면 **이미지 재빌드 없이** 앱에 반영됩니다.
- **requirements.txt 변경**(새 패키지 추가) 시에는 `docker compose build --no-cache` 등으로 **이미지 재빌드**가 필요합니다.
- Dockerfile의 `CMD`(gunicorn)는 **compose의 command에 의해 덮어써져서** 사용되지 않습니다.

---

## 3. 프로덕션 환경 (가정)

| 항목 | 설정 | 목적 |
|------|------|------|
| **FastAPI volumes** | 제거 | 이미지 안에 코드 포함, 외부 마운트 없음 |
| **FastAPI command** | 제거 | Dockerfile의 `CMD` 사용 (gunicorn) |
| **Postgres ports** | 노출 최소화 또는 제거 | DB는 내부 네트워크만 (보안) |
| **docs_url** | `None` | API 문서 비노출 |
| **root_path** | `""` 또는 실제 앞단 경로 | Nginx/ALB 등 실제 경로에 맞춤 |

**Dockerfile CMD (프로덕션)**

```dockerfile
CMD ["gunicorn", "main.app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
```

- gunicorn이 **4개의 uvicorn 워커**로 `main.app:app`을 8080에 바인딩합니다.
- 프로덕션에서는 `volumes`로 소스를 덮어쓰지 않고, **빌드 시점에 복사된 코드**만 사용합니다.

---

## 4. uvicorn vs gunicorn (개념)

| 구분 | uvicorn | gunicorn |
|------|---------|----------|
| **역할** | ASGI 서버. FastAPI 앱 실행 | 프로세스 관리자. 여러 워커 실행 |
| **동시성** | 이벤트 루프 기반 (concurrency) | 여러 프로세스 (parallelism) |
| **개발** | `uvicorn app:app --reload` | 사용 안 함 |
| **프로덕션** | gunicorn의 worker로 사용 | `--workers 4`, `UvicornWorker` |

- **Concurrency**: uvicorn 하나가 여러 요청을 이벤트 드라이브로 처리.
- **Parallelism**: gunicorn이 여러 uvicorn 프로세스를 띄워 CPU 코어를 나눠 씀.

---

## 5. 체크리스트 (배포 전)

- [ ] `docs_url=None`, `root_path` 실제 경로로 설정
- [ ] FastAPI 서비스에서 `volumes`, `command` 제거 후 이미지 빌드·실행
- [ ] `.env` 등 비밀값은 보안 관리 (시크릿/환경 변수)
- [ ] Postgres 포트 외부 노출 여부 재검토
- [ ] Nginx(또는 ALB) SSL/TLS, 로그, 제한 등 운영 설정

---

## 6. 요약

| 구분 | 개발 | 프로덕션 |
|------|------|----------|
| **코드 반영** | 볼륨 마운트 + uvicorn --reload | 이미지 빌드, gunicorn CMD |
| **API 문서** | `/docs` 사용 | 비노출 |
| **DB 포트** | 5001 노출 (도구 접속) | 내부 전용 권장 |
| **실행 방식** | uvicorn 단일 프로세스 | gunicorn + uvicorn 워커 다중 프로세스 |

이 문서들은 docker-compose로 구성된 백엔드 전체 구조와 개념을 설명합니다.  
추가로 필요한 부분이 있으면 해당 문서를 확장하면 됩니다.
