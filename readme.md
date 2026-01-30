# 전체 구조
- db
    - postgres
- server
    - fastapi, pydantic, SQLModel
- nginx

# 동작
1. 사용자의 요청을 받아 nginx는 내부 컨테이너 중 적절한 컨테이너를 선택해 요청을 날림
2. 내부 컨테이너 중에서 fastapi 컨테이너는 사용자의 응답에 따라 데이터를 get, post, put, delete함
3. 이 때 fastapi 컨테이너는 postgres와 상호작용 함

# gunicorn과 uvicorn
- 기본적으로 fastAPI는 비동기식 프레임 워크로 ASGI라는 프로토콜 위에서 동작
- 또한 fastAPI는 비지니스 로직 정의를 도와줄 뿐 실제 동작을 하는 주체는 아님
- 이에 따라 fastAPI는 ASGI 프로토콜 위에서 동작하는 wrapper가 필요하고 이러한 wrapper가 바로 uvivorn
- uvicorn은 fastAPI에 정의된 비지니즈 로직에 따라 event driven으로 동작 (하나의 스레드가 이벤트 큐에 요청이 쌓일 때 마다 이를 순차적을 처리)
- 결국 uvicorn + fastAPI는 단일 스레드로 동작하기 때문에 클라이언트가 많아지면 느려질 수 밖에 없음 (CPU 코어의 일부만 사용하는 상태)
- gunicorn은 uvicorn+fastAPI를 프로세스(워커) 단위로 동작시키는 라이브러리로 간단한 설정만으로 CPU를 효율적으로 활용하도록 도와줌
- 더 자세히 알고 싶으면 gunicorn은 parellalism, uvicorn+fastAPi는 concurrency라는 내용을 더 파고드는게 좋음 (개발자 면접 필수 질문 중 하나)

# 주의 깊게 보아야 할 것들
1. docker-compose.yml 구성은 어떻게 되어 있는지
2. fastapi 빌드시 사용하는 Dockerfile은 어떻게 되어 있는지
3. 개발을 위해서 docker-compose.yml, faseapi main/app.py가 어떻게 구성되어 있는지
4. nginx의 프록시 설정이 어떻게 되어 있는지
5. 전체 프로젝트 폴더가 어떻게 구성되고 docker-compose.yml에 의해 구동되게 되는지
6. postgres DB와 fastAPI가 어떻게 상호작용 하는지