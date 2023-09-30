if [[ -f .env ]]; then
    export $(cat .env | xargs)
fi

docker_base_dir="/opt/${SERVER_NAME}"
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin ${AWS_ECR_URL}

docker buildx build --build-arg DIR=$docker_base_dir --platform=linux/amd64 -t ${SERVER_NAME} .
docker tag ${SERVER_NAME}:latest ${AWS_ECR_URL}/${SERVER_NAME}:latest
docker push ${AWS_ECR_URL}/comfort:latest