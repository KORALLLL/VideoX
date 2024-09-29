FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    python3-pip \
    ffmpeg \
    libsm6 \
    libxext6 \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt