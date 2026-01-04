FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Корень проекта
WORKDIR /opt/ml_api

# Добавляем оба пути. ВАЖНО: корень нужен для импорта модели,
# а путь к Credit_Api — чтобы работал 'from app'
ENV PYTHONPATH=/opt/ml_api:/opt/ml_api/Credit_Api
ENV PYTHONUNBUFFERED=1

# 1. Зависимости МОДЕЛИ
COPY requirements/ /opt/ml_api/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/requirements.txt

# 2. Зависимости API
COPY Credit_Api/requirements.txt /opt/ml_api/Credit_Api_requirements.txt
RUN pip install --no-cache-dir -r /opt/ml_api/Credit_Api_requirements.txt

# Копируем всё содержимое
COPY . .

# Меняем WORKDIR на папку с API перед запуском
# Это гарантирует, что 'app' будет в текущей папке для uvicorn
WORKDIR /opt/ml_api/Credit_Api

RUN adduser --disabled-password --gecos '' ml-api-user && \
    chown -R ml-api-user:ml-api-user /opt/ml_api
USER ml-api-user

EXPOSE 8000

# Запускаем из папки Credit_Api, поэтому путь теперь просто app.main:app
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
