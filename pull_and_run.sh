if [[ -f .env ]]; then
    export $(cat .env | xargs)
fi

docker stop comfort ; docker rm comfort ; docker rmi ${AWS_ECR_URL}/comfort ; docker rmi comfort

aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin ${AWS_ECR_URL}
docker pull ${AWS_ECR_URL}/comfort:latest

docker tag ${AWS_ECR_URL}/comfort:latest comfort:latest
docker run --name comfort --restart=always -v $PWD/logs:/opt/comfort/logs -d -p ${PORT}:${PORT} comfort:latest