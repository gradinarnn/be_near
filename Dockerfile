FROM python:latest

RUN mkdir -p /usr/src/app/web
WORKDIR /usr/src/app/web

COPY . /usr/src/app/web

RUN pip install -r requirements.txt


ENTRYPOINT["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]