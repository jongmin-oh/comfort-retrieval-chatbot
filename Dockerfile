# 베이스 이미지
FROM python:3.9.9-buster

#설치시 질문 안나오게 설정
ARG DEBIAN_FRONTEND=noninteractive

# apt 업데이트
RUN apt-get update

# 패키지 설치
RUN apt-get install -y curl git g++

# 파이썬 설치
RUN apt-get install -y python3 python3-pip

# 소스코드 복사
COPY . /opt/comfort-bot

#작업 폴더 설정
WORKDIR /opt/comfort-bot

#PyTorch 설치
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# 파이썬 패키지 설치
RUN pip3 install -r requirements.txt

# 실행
CMD ["python3","server.py"]