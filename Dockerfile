# syntax=docker/dockerfile:1
FROM python:3.8.10
ENV PYTHONBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt