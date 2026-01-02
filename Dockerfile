FROM python:3.10-slim

# Создаем пользователя для безопасности
RUN adduser --disabled-password --gecos '' ml-api-user
WORKDIR /opt/ml_api

# 1. Копируем requirements из папки Credit_Api
COPY ./Credit_Api/requirements.txt /opt/ml_api/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/ml_api/requirements.txt

# 2. Копируем пакет с логикой модели
COPY ./classification_model /opt/ml_api/classification_model

# 3. Копируем папку с FastAPI (она внутри Credit_Api)
COPY ./Credit_Api/app /opt/ml_api/app

# Настраиваем права доступа
RUN chown -R ml-api-user:ml-api-user /opt/ml_api
USER ml-api-user

# Открываем порт для FastAPI
EXPOSE 8001

# Запуск через uvicorn (путь к приложению внутри контейнера)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
