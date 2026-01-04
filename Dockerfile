FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем корень проекта
WORKDIR /opt/ml_api

# Добавляем корень И папку API в PYTHONPATH
# Это позволит работать импортам 'from app' и 'from classification_model'
ENV PYTHONPATH=/opt/ml_api:/opt/ml_api/Credit_Api
ENV PYTHONUNBUFFERED=1

# 1. Установка зависимостей всей системы (MLOPS/requirements)
COPY requirements/ /opt/ml_api/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/requirements.txt

# 2. Установка зависимостей API (Credit_Api/requirements.txt)
COPY Credit_Api/requirements.txt /opt/ml_api/Credit_Api_requirements.txt
RUN pip install --no-cache-dir -r /opt/ml_api/Credit_Api_requirements.txt

# Копируем проект
COPY . .

RUN adduser --disabled-password --gecos '' ml-api-user && \
    chown -R ml-api-user:ml-api-user /opt/ml_api
USER ml-api-user

EXPOSE 8000

# Запуск модуля uvicorn через полный путь от корня
CMD ["python", "-m", "uvicorn", "Credit_Api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
