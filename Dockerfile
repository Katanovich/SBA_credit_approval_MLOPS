FROM python:3.10-slim

# Создаем пользователя
RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /opt/ml_api

# Устанавливаем зависимости
COPY ./requirements.txt /opt/ml_api/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/ml_api/requirements.txt

# Копируем пакет с моделью и само API
COPY ./classification_model /opt/ml_api/classification_model
COPY ./app /opt/ml_api/app

# Настраиваем права
RUN chown -R ml-api-user:ml-api-user /opt/ml_api
USER ml-api-user

EXPOSE 8001

# Запуск FastAPI (предполагаем, что файл main.py лежит в папке app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]