FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем базовую рабочую директорию
WORKDIR /opt/ml_api

# Настройка путей, чтобы Python видел все папки как модули
ENV PYTHONPATH=/opt/ml_api:/opt/ml_api/Credit_Api
ENV PYTHONUNBUFFERED=1

# Установка зависимостей из корня
COPY requirements/ /opt/ml_api/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/requirements.txt

# Установка зависимостей специфичных для Credit_Api
COPY Credit_Api/requirements.txt /opt/ml_api/Credit_Api_requirements.txt
RUN pip install --no-cache-dir -r /opt/ml_api/Credit_Api_requirements.txt

# Копируем весь проект целиком
COPY . .

# Создаем пользователя для безопасности
RUN adduser --disabled-password --gecos '' ml-api-user && \
    chown -R ml-api-user:ml-api-user /opt/ml_api
USER ml-api-user

EXPOSE 8000

# Запуск: используем полный путь Credit_Api.app.main
# Это позволит импорту "from app.api" внутри main.py найти папку app
CMD ["sh", "-c", "python -m uvicorn Credit_Api.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
