FROM python:3.11

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# requirements,txt를 복사해온 다음 필요 패키지 설치
COPY server/main/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 호스트의 server/main 폴더 내용을 컨테이너의 현재 작업 위치인 /app으로 폴더를 복사
COPY server/main/ ./


# 컨테이너가 8080 포트를 리스닝함을 명시(문서화)
EXPOSE 8080

# main.app:app = main/app.py 안의 app 객체를 Gunicorn(UvicornWorker)로 실행
CMD ["gunicorn", "main.app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]