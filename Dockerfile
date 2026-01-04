FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/ml_api

# ВАЖНО: Добавляем Credit_Api в пути, чтобы папка 'app' была видна как модуль
ENV PYTHONPATH=/opt/ml_api:/opt/ml_api/Credit_Api
ENV PYTHONUNBUFFERED=1

# Установка зависимостей
COPY requirements/ /opt/ml_api/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/requirements.txt

COPY Credit_Api/requirements.txt /opt/ml_api/Credit_Api_requirements.txt
RUN pip install --no-cache-dir -r /opt/ml_api/Credit_Api_requirements.txt

# Копируем проект
COPY . .

# Переходим в папку, где лежит папка 'app'
WORKDIR /opt/ml_api/Credit_Api

RUN adduser --disabled-password --gecos '' ml-api-user && \
    chown -R ml-api-user:ml-api-user /opt/ml_api
USER ml-api-user

EXPOSE 8000

# Запускаем через модуль uvicorn.
# Так как мы в /opt/ml_api/Credit_Api, он увидит папку 'app'
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
