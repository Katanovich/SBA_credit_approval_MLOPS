FROM python:3.10-slim

# Создаем пользователя для безопасности
RUN adduser --disabled-password --gecos '' ml-api-user

# ВНУТРЕННИЙ путь в контейнере (не меняй его на путь к рабочему столу!)
WORKDIR /opt/ml_api

# Переменные окружения
ENV PYTHONPATH=/opt/ml_api

# 1. Копируем requirements (относительно корня проекта MLOPS)
# Находимся в папке MLOPS -> заходим в Credit_Api
COPY ./Credit_Api/requirements.txt /opt/ml_api/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/ml_api/requirements.txt

# 2. Копируем модель
COPY ./classification_model /opt/ml_api/classification_model

# 3. Копируем всё из Credit_Api в текущий WORKDIR (/opt/ml_api)
COPY ./Credit_Api /opt/ml_api/

# Настраиваем права доступа
RUN chown -R ml-api-user:ml-api-user /opt/ml_api
RUN chmod +x /opt/ml_api/run.sh

USER ml-api-user

# Открываем порт для FastAPI
EXPOSE 8001

# Запуск (uvicorn ищет папку app в текущем WORKDIR)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
