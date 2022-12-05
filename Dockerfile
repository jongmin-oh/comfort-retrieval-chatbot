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
COPY . /opt/elastic_chatbot

#작업 폴더 설정
WORKDIR /opt/elastic_chatbot

# 파이썬 패키지 설치
RUN pip3 install -r requirements.txt

CMD ["python3","server.py"]