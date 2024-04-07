FROM python:3.11.5-slim

#설치시 질문 안나오게 설정
ARG DEBIAN_FRONTEND=noninteractive

# 디렉터리 생성
RUN mkdir /opt/app

# 소스코드 복사
COPY . /opt/app

#작업 폴더 설정
WORKDIR /opt/app

# 파이썬 패키지 설치
RUN pip install -r requirements.txt

# 실행
CMD ["gunicorn", "manage:app", "-c", "gunicorn.conf.py"]