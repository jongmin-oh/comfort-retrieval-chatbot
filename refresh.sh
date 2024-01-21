#!/bin/bash

# .env 파일 로드
if [[ -f .env ]]; then
    export $(cat .env | xargs)
fi

echo "기존 ${SERVER_NAME} 서버를 중지합니다."

# container_name="combot"
docker stop ${SERVER_NAME} ; docker rm ${SERVER_NAME} ; docker rmi ${SERVER_NAME}

echo "새로운 ${SERVER_NAME} 서버를 빌드합니다."
docker build -t ${SERVER_NAME} .

echo "새로운 ${SERVER_NAME} 서버를 시작합니다."
docker run --name ${SERVER_NAME} --restart=always --network=bridge -v $PWD:/opt/app -d -p ${PORT}:${PORT} ${SERVER_NAME}:latest

echo "이전 ${SERVER_NAME} 이미지를 삭제합니다."
docker system prune -af

docker logs ${SERVER_NAME} --tail 20 -f