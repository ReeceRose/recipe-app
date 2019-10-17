FROM python:3.6-alpine3.9

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r /requirements.txt

RUN mkdir /api
WORKDIR /api
COPY ./api /api

RUN adduser -D user
USER user