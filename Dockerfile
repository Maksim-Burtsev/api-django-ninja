FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt