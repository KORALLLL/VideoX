# VideoX Backend

## Установка и запуск проекта

Скачайте репозиторий проекта:

```bash
git clone https://github.com/KORALLLL/VideoX.git
```

Создайте файл `config.toml` чтобы развернуть проект на локальной машине или `docker_config.toml` для развёртывания с помощью `docker-compose` в папке репозитория с подобным наполнением

```toml
[app]
bind_addr = "http://localhost:8000"
bind_host = "0.0.0.0"
bind_port = 8000

[s3]
aws_host = "http://localhost:9000"
aws_bucket = "<YOUR_AWS_BUCKET>"
aws_access_key = "<YOUR_AWS_ACCESS_KEY>"
aws_secret_access_key = "<YOUR_AWS_SECRET_ACCESS_KEY>"

[database]
postgres_username = "<YOUR_POSTGRES_USERNAME>"
postgres_db = "<YOUR_POSTGRES_DB>"
postgres_port = 5432
postgres_host = "localhost"
postgres_password = "<YOUR_POSTGRES_PASSWORD>"
```

Также возможно предварительно настроить параметры в `docker-compose.yml`

## Запуск

Запустите проект с помощью `python`

```bash
python -m src
```

Или с помощью `docker compose`

```bash
docker-compose up --build -d
```
