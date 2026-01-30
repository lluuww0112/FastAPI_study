# 01. 전체 아키텍처 개요

## 1. 구성 요소

이 프로젝트는 **3개의 서비스**가 Docker Compose로 묶여 동작합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Docker Compose Network                      │
│                                                                 │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐   │
│  │    Nginx     │      │   FastAPI    │      │  PostgreSQL  │   │
│  │  (리버스       │ ───► │  (API 서버)   │ ───► │   (DB)       │   │
│  │   프록시)      │      │  uvicorn     │      │   postgres   │   │ 
│  │   :80        │      │   :8080      │      │   :5000      │   │
│  └──────┬───────┘      └──────────────┘      └──────────────┘   │
│         │                                                       │
└─────────┼───────────────────────────────────────────────────────┘
          │
          │ :80 (호스트에 노출)
          ▼
    ┌──────────┐
    │ 클라이언트 │
    └──────────┘
```

| 서비스 | 역할 | 호스트 노출 포트 | 컨테이너 내부 포트 |
|--------|------|------------------|---------------------|
| **nginx** | 리버스 프록시, 요청 라우팅 | 80 | 80 |
| **fastapi** | REST API (CRUD), 비즈니스 로직 | (없음, nginx 경유) | 8080 |
| **postgres** | 관계형 DB, 데이터 저장 | 5001 (개발용 DBeaver 등) | 5000 |

- 클라이언트는 **80번 포트**만 사용합니다.
- FastAPI는 **내부 네트워크**에서만 `fastapi:8080`으로 접근됩니다.
- PostgreSQL은 **내부**에서는 `postgres:5000`, **호스트에서**는 `localhost:5001`로 접근합니다.

---

## 2. 디렉터리 구조

```
fastAPI_withDB/
├── docker-compose.yml      # 서비스·볼륨 정의
├── .env                     # 공통 환경 변수 (DB, 포트 등)
│
├── nginx/
│   └── nginx.conf          # 리버스 프록시 설정
│
├── server/
│   ├── Dockerfile          # FastAPI 이미지 빌드
│   ├── .env                # FastAPI 전용 환경 변수
│   └── main/               # FastAPI 애플리케이션 코드
│       ├── app.py          # 앱 진입점, 라우터 등록
│       ├── util.py         # DB 엔진, 세션, 테이블 생성
│       ├── requirements.txt
│       ├── models/         # SQLModel 모델 (Student, College)
│       └── Routers/        # API 라우터 (get, post, put, delete)
│
├── db/
│   └── postgresql.conf     # PostgreSQL 설정 (포트, 인코딩 등)
│
├── architecture/           # 이 문서들이 있는 디렉터리
├── example/                 # FastAPI 학습용 단계별 예제
└── readme.md
```

**개념 정리**

- **docker-compose.yml**: 어떤 컨테이너를 어떻게 띄울지, 볼륨·포트·의존성을 정의.
- **nginx**: “문지기”. 80번으로 들어온 요청 중 `/main_server/`를 FastAPI로 넘김.
- **server/main**: 실제 API 로직. DB는 `util.py`에서 연결하고, 라우터는 `app.py`에서 등록.
- **db**: PostgreSQL 설정 파일만 두고, 데이터는 Docker volume에 저장.

---

## 3. 핵심 개념 요약

| 개념 | 설명 |
|------|------|
| **리버스 프록시** | Nginx가 클라이언트 요청을 받아, 내부 서버(FastAPI)로 전달하고 응답을 다시 클라이언트에게 돌려줌. |
| **서비스 디스커버리** | 같은 Compose 네트워크 안에서는 **서비스 이름**(`fastapi`, `postgres`)으로 호스트명 사용. |
| **의존성 순서** | Nginx → FastAPI → Postgres. Postgres가 healthy 된 뒤 FastAPI가 뜨고, 그 다음 Nginx가 동작. |
| **root_path** | FastAPI는 `root_path="/main_server"`로 설정되어, Nginx 앞단 경로와 Swagger 등 문서 경로를 맞춤. |

다음 문서에서는 **Docker Compose** 설정을 자세히 다룹니다.
