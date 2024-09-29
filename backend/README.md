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



# Документация по хэндлерам API

## 1. `handle_polling`

### Описание
Этот хэндлер обрабатывает запросы на получение нового видео для обработки, основываясь на имени модели.

### Параметры
- **Path параметр:**
  - `model_name` (str): Имя модели, для которой запрашивается новое видео.

- **Query параметры:**
  - Нет.

- **Body параметры:**
  - Нет.

### Пример ответа
```JSON
{
  "video_url": "string",
  "video_callback_url": "string",
  "json_callback_url": "string"
}
{
  "video_url": "string",
  "video_callback_url": "string",
  "json_callback_url": "string"
}
```

### Пример запроса
```
GET /api/v1/poll/yolo
```

---

## 2. `handle_get_all_videos`

### Описание
Этот хэндлер возвращает список всех видео, отсортированных по убыванию их идентификаторов.

### Параметры
- **Path параметры:**
  - Нет.

- **Query параметры:**
  - Нет.

- **Body параметры:**
  - Нет.

### Пример ответа
```JSON
{
  "count": 0,
  "result": [
    {
      "id": 0,
      "name": "string",
      "created_at": "2024-09-29T02:48:16.534Z",
      "image_url": "string",
      "status": "CREATED"
    }
  ]
}
```


### Пример запроса
```
GET /api/v1/video
```

---

## 3. `handle_get_video_by_id`

### Описание
Этот хэндлер возвращает JSON-данные, связанные с видео по его идентификатору.

### Параметры
- **Path параметры:**
  - `video_id` (int): Идентификатор видео.

- **Query параметры:**
  - Нет.

- **Body параметры:**
  - Нет.

### Пример ответа
```JSON
{
  "id": 0,
  "name": "string",
  "status": "CREATED",
  "uploaded_at": "2024-09-29T02:50:52.314Z",
  "processed_at": "2024-09-29T02:50:52.314Z",
  "original_video_url": "string",
  "processed_video_url": "string",
  "processed": {}
}
```

### Пример запроса
```
GET /api/v1/video/1/json
```

---


## 4. `handle_upload_video`

### Описание
Этот хэндлер обрабатывает загрузку нового видео.

### Параметры
- **Path параметры:**
  - Нет.

- **Query параметры:**
  - name - название видео

- **Body параметры:**
  - `video` - Файл видео для загрузки.

### Пример ответа
```JSON
{
  "id": 0,
  "name": "string",
  "status": "CREATED",
  "created_at": "2024-09-29T02:53:42.291Z",
  "uploaded_at": "2024-09-29T02:53:42.291Z",
  "original_video_path": "string",
  "processed_video_path": "string",
  "original_video_link": "string",
  "processed_video_link": "string",
  "original_preview_path": "string",
  "preview_link": "string"
}
```

### Пример запроса
```
POST /api/v1/video
```

---

## 5. `handle_upload_resulted_video`

### Описание
Этот хэндлер обрабатывает загрузку обработанного видео по его идентификатору.

### Параметры
- **Path параметры:**
  - `video_id` (int): Идентификатор видео.

- **Query параметры:**
  - Нет.

- **Body параметры:**
  - `video`: Файл обработанного видео для загрузки.

### Пример ответа
- **str**: URL загруженного видео.

### Пример запроса
```
POST /api/v1/video/1/upload/video
```

---

## 6. `handle_upload_json_result`

### Описание
Этот хэндлер обрабатывает загрузку JSON-результатов для видео по его идентификатору и имени модели.

### Параметры
- **Path параметры:**
  - `video_id` (int): Идентификатор видео.
  - `model_name` (str): Имя модели.

- **Query параметры:**
  - Нет.

- **Body параметры:**
  - `json` (dict): Объект JSON с результатами обработки.

### Пример ответа
- **None**: Успешное выполнение без возвращаемого значения.

### Пример запроса
```
POST /api/v1/video/1/upload/json/yolo
```
