FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в корень проекта
WORKDIR /opt/ml_api

# Важно: добавляем обе папки в пути поиска модулей
ENV PYTHONPATH=/opt/ml_api:/opt/ml_api/Credit_Api
ENV PYTHONUNBUFFERED=1

# Установка зависимостей
COPY requirements/ /opt/ml_api/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/requirements.txt

COPY Credit_Api/requirements.txt /opt/ml_api/Credit_Api_requirements.txt
RUN pip install --no-cache-dir -r /opt/ml_api/Credit_Api_requirements.txt

# Копируем весь код
COPY . .

# Настройка прав доступа
RUN adduser --disabled-password --gecos '' ml-api-user && \
    chown -R ml-api-user:ml-api-user /opt/ml_api
USER ml-api-user

EXPOSE 8000

# ГЛАВНОЕ ИЗМЕНЕНИЕ:
# 1. Мы заходим в папку Credit_Api (где лежит папка app)
# 2. Запускаем через -m uvicorn app.main:app
# Это заставит относительные импорты (from .api) работать.
WORKDIR /opt/ml_api/Credit_Api

CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
