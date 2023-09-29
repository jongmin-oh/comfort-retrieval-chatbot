#!/bin/bash

# .env 파일 로드
if [[ -f .env ]]; then
    export $(cat .env | xargs)
fi

docker_base_dir="/opt/${SERVER_NAME}"
echo "${SERVER_NAME} 서버를 실행합니다."

docker run --name ${SERVER_NAME} --restart=always -v $PWD:$docker_base_dir -d -p ${PORT}:${PORT} ${SERVER_NAME}:latest
docker logs ${SERVER_NAME} --tail 20 -f