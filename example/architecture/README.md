# 백엔드 프로젝트 아키텍처

이 디렉토리는 **docker-compose**로 구성된 백엔드 전체 프로젝트의 구조와 개념을 설명합니다.

---

## 문서 목차

| 문서 | 설명 |
|------|------|
| [01-overview.md](./01-overview.md) | 전체 아키텍처 개요, 구성 요소, 디렉터리 구조 |
| [02-docker-compose.md](./02-docker-compose.md) | Docker Compose 설정, 서비스 정의, 볼륨·네트워크 |
| [03-nginx.md](./03-nginx.md) | Nginx 리버스 프록시, upstream, location 설정 |
| [04-fastapi-server.md](./04-fastapi-server.md) | FastAPI 애플리케이션, Dockerfile, 라이프사이클 |
| [05-postgres.md](./05-postgres.md) | PostgreSQL 설정, healthcheck, 데이터 영속성 |
| [06-data-flow.md](./06-data-flow.md) | 요청/응답 흐름, 포트·경로 매핑 |
| [07-development-vs-production.md](./07-development-vs-production.md) | 개발 환경 vs 프로덕션 환경 차이 |

---

## 빠른 참조

```
[클라이언트] → :80 → [Nginx] → /main_server/* → [FastAPI :8080] → [PostgreSQL :5000]
```

| 접속 목적 | URL / 호스트:포트 |
|-----------|-------------------|
| API (Swagger 문서) | `http://localhost/main_server/docs` |
| API (예: health) | `http://localhost/main_server/health` |
| DB (DBeaver 등) | `localhost:5001` → 컨테이너 내부 `5000` |

---

## 관련 파일 위치

| 역할 | 경로 |
|------|------|
| Compose 정의 | `./docker-compose.yml` |
| Nginx 설정 | `./nginx/nginx.conf` |
| FastAPI 앱 | `./server/main/` |
| FastAPI Dockerfile | `./server/Dockerfile` |
| PostgreSQL 설정 | `./db/postgresql.conf` |
| 환경 변수 | `./.env`, `./server/.env` |

---

## 학습 시 참고할 순서

1. **01-overview** → 전체 그림 파악  
2. **02-docker-compose** → 서비스·의존성·볼륨 이해  
3. **06-data-flow** → 요청이 Nginx → FastAPI → DB로 어떻게 흐르는지  
4. **03-nginx**, **04-fastapi-server**, **05-postgres** → 각 컴포넌트 상세  
5. **07-development-vs-production** → 개발/배포 차이 정리
