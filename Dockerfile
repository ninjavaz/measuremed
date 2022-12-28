# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "measuremed.wsgi"]




# # syntax=docker/dockerfile:1
# FROM python:3.8.10
# ENV PYTHONBUFFERED=1
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt




# version: "3.8"
# services:
#   app:
#     build: .
#     volumes:
#       - .:/app
#     ports:
#       - 8000:8000
#     image: ninjavaz/notifymed-app:latest
#     container_name: notifymed_app_container
#     command: python notifymed/manage.py runserver 0.0.0.0:8000
#   redis:
#     image: "redis:alpine"
#     ports:
#      - "6379:6379" 
#     container_name: notifymed_redis_container
#   django-q:
#     build: .
#     image: ninjavaz/notifymed-djangoq:latest
#     container_name: notifymed_djangoq_container
#     command: python notifymed/manage.py qcluster
#     volumes:
#       - .:/app
#     depends_on:
#       - redis
    