FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt