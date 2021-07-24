  GNU nano 4.8                       Dockerfile                       Modified

FROM python:latest

RUN mkdir -p /usr/src/app/web
WORKDIR /usr/src/app/web

COPY . /usr/src/app/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install -r requirements.txt

COPY . .


