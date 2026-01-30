# 03. Nginx (리버스 프록시)

## 1. Nginx의 역할

**Nginx**는 이 프로젝트에서 **리버스 프록시**로 동작합니다.

- **클라이언트**는 Nginx의 **80번 포트**로만 요청을 보냅니다.
- Nginx는 요청 경로에 따라 **내부 서버(FastAPI)**로 **전달(proxy)**하고, 응답을 다시 클라이언트에게 돌려줍니다.
- FastAPI 컨테이너는 **외부에 포트를 노출하지 않고**, Nginx를 통해서만 접근됩니다.

```
클라이언트  →  [Nginx :80]  →  [FastAPI :8080]
                ↑
            유일한 입구
```

---

## 2. nginx.conf 구조

### 2.1 upstream: 백엔드 서버 그룹

```nginx
upstream main_server {
    server fastapi:8080;
}
```

| 항목 | 의미 |
|------|------|
| `main_server` | 이 그룹의 이름 (아래 `location`에서 사용) |
| `fastapi:8080` | Docker Compose 서비스 이름 `fastapi`의 8080 포트 |
| `least_conn;` (주석) | 넣으면 연결 수가 적은 서버로 로드밸런싱. 서버가 하나면 생략 가능 |

- 같은 네트워크 안이므로 **서비스 이름(`fastapi`)**으로 접근합니다.
- 나중에 FastAPI 인스턴스를 여러 개 두면 `server fastapi1:8080;`, `server fastapi2:8080;` 처럼 추가할 수 있습니다.

---

### 2.2 server / location: 경로별 라우팅

```nginx
server {
    listen 80;

    location /main_server/ {
        rewrite            ^/main_server(.*)$ $1 break;
        proxy_pass         http://main_server;
        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
    }
}
```

**동작 요약**

1. **`listen 80`**  
   Nginx는 80번 포트로 들어오는 요청을 받습니다.

2. **`location /main_server/`**  
   URL이 `/main_server/`로 시작하는 요청만 이 블록에서 처리합니다.

3. **`rewrite ^/main_server(.*)$ $1 break;`**  
   - 들어온 경로: `/main_server/get/student`  
   - `(.*)`에 해당하는 부분: `/get/student`  
   - **`$1`**로 치환 후 **break** → Nginx가 **내부적으로** `http://main_server/get/student` 로 요청을 보냅니다.  
   즉, **클라이언트에게 보내는 URL은 그대로 `/main_server/...`**이고, **FastAPI에는 `/main_server` 접두사 없이** `/get/student`만 전달됩니다.

4. **`proxy_pass http://main_server;`**  
   위에서 만든 경로(`/get/student`)로 `main_server`(즉 `fastapi:8080`)에 프록시합니다.

5. **`proxy_set_header`**  
   - `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Host`를 넘겨서, FastAPI가 “실제 클라이언트 IP”나 “원래 Host”를 알 수 있게 합니다.

---

## 3. URL 변환 정리

| 클라이언트가 요청한 URL | Nginx가 FastAPI로 보내는 URL |
|------------------------|------------------------------|
| `http://localhost/main_server/health` | `http://fastapi:8080/health` |
| `http://localhost/main_server/docs` | `http://fastapi:8080/docs` |
| `http://localhost/main_server/get/student` | `http://fastapi:8080/get/student` |

- **클라이언트**는 항상 **`/main_server/...`** 를 사용합니다.
- **FastAPI**는 **`/main_server` 없이** `/health`, `/docs`, `/get/student` 등만 받습니다.
- 그래서 FastAPI 쪽에서는 `root_path="/main_server"`만 설정해 두고, **라우트는 모두 `/...` 로만** 정의합니다.

---

## 4. FastAPI의 root_path

`server/main/app.py` 예시:

```python
root_path = "/main_server" if mode == "dev" else ""

app = FastAPI(
    root_path=root_path,
    ...
)
```

- **root_path**는 “이 앱이 어떤 URL 접두사 아래에 서빙되는지”를 알려주는 값입니다.
- Nginx가 `/main_server`를 제거하고 보내므로, FastAPI는 **경로상으로는** `/docs`, `/get/student`만 받지만, **문서(Swagger)에서는** “실제 클라이언트가 호출할 URL”을 `https://localhost/main_server/docs`처럼 보여주기 위해 `root_path`를 사용합니다.

---

## 5. keepalive / 로그 (참고)

```nginx
keepalive_timeout 65s;
```

- 클라이언트와 Nginx 사이 TCP 연결을 65초 동안 유지합니다.
- `access_log`, `error_log`는 기본 경로(`/var/log/nginx/...`)에 남습니다. 필요하면 `log_format`과 함께 커스터마이즈할 수 있습니다.

---

## 6. 정리

| 주체 | 사용하는 URL / 경로 |
|------|----------------------|
| **클라이언트** | `http://localhost/main_server/...` |
| **Nginx** | 받은 요청에서 `/main_server` 제거 후 `http://fastapi:8080/...` 로 전달 |
| **FastAPI** | `/health`, `/docs`, `/get/...` 등 (root_path는 문서/OpenAPI용) |

다음 문서에서는 **FastAPI 서버** 구조(Dockerfile, app, util, 라우터)를 다룹니다.
