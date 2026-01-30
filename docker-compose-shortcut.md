## 전체 컨테이너 및 이미지 삭제 후 재빌드
docker compose down -v
docker rm -f $(docker ps -a -q)
docker rmi $(docker images -a)
docker volume prune
docker images
docker ps -a
docker volume ls

# 시스템 내에 현재 남아 있는 컨테이너 및 이미지, 볼륨 확인
docker images
docker ps -a
docker volume ls
