FROM python:3.11

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# requirements,txt를 복사해온 다음 필요 패키지 설치
COPY server/main/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 호스트의 server/main 폴더 내용을 컨테이너의 현재 작업 위치인 /app으로 폴더를 복사
COPY server/main/ ./


# fastapi의 내부 포트 개방
# 도커 컴포즈 네트워크에 속하는 컨테이너만 해당 포트로 접속할 수 있음
EXPOSE 8080

# 5. 실행 명령
# 위에서 WORKDIR로 /app을 설정했으니 현재 경로는 fasetapi컨테이너 내의 /app임
# server/main의 모든 파일을 컨테이너의 /app/main으로 복사했으니 
# main/main.py에서 정의한 app.py의 app을 uvicorn으로 감싸고 gunicorn으로 프로세스 단위로 실행하기 위한 커맨드가 아래 내용임
CMD ["gunicorn", "main.app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]