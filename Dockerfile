FROM python:3.10-slim

# Создаем пользователя для безопасности
RUN adduser --disabled-password --gecos '' ml-api-user

# ВНУТРЕННИЙ путь в контейнере
WORKDIR /opt/ml_api

# Переменные окружения
ENV PYTHONPATH=/opt/ml_api

# 1. Копируем и устанавливаем зависимости
COPY ./Credit_Api/requirements.txt /opt/ml_api/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/ml_api/requirements.txt

# 2. Копируем модель и API
COPY ./classification_model /opt/ml_api/classification_model
COPY ./Credit_Api /opt/ml_api/

# 3. Настраиваем права (УДАЛИЛИ СТРОКУ С CHMOD RUN.SH)
RUN chown -R ml-api-user:ml-api-user /opt/ml_api

USER ml-api-user

# Открываем порт для FastAPI
EXPOSE 8001

# Запуск напрямую
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
