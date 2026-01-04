FROM python:3.10-slim

# Установка системных утилит для сборки (нужны для xgboost/pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория в корне контейнера
WORKDIR /opt/ml_api

# Настройка путей для корректных импортов
ENV PYTHONPATH=/opt/ml_api:/opt/ml_api/Credit_Api
ENV PYTHONUNBUFFERED=1

# 1. Устанавливаем зависимости ВСЕГО пакета (модели)
# Копируем структуру папок для requirements
COPY requirements/ /opt/ml_api/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/requirements.txt

# 2. Устанавливаем зависимости самого API
COPY Credit_Api/requirements.txt /opt/ml_api/Credit_Api_requirements.txt
RUN pip install --no-cache-dir -r /opt/ml_api/Credit_Api_requirements.txt

# Копируем весь исходный код проекта
COPY . .

# Настройка безопасности
RUN adduser --disabled-password --gecos '' ml-api-user && \
    chown -R ml-api-user:ml-api-user /opt/ml_api

# Переходим в папку API для запуска uvicorn
WORKDIR /opt/ml_api/Credit_Api

USER ml-api-user

EXPOSE 8000

# Запуск через python -m гарантирует, что 'app' будет виден как модуль
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
