FROM python:3.12

WORKDIR /notify_service

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .