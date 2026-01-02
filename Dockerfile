FROM python:3.10-slim

RUN adduser --disabled-password --gecos '' ml-api-user
WORKDIR /opt/ml_api

# Копируем из правильной папки Credit_Api
COPY ./Credit_Api/requirements.txt /opt/ml_api/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/ml_api/requirements.txt

# Копируем код
COPY ./classification_model /opt/ml_api/classification_model
COPY ./Credit_Api/app /opt/ml_api/app

RUN chown -R ml-api-user:ml-api-user /opt/ml_api
USER ml-api-user

EXPOSE 8001

# Обрати внимание на путь к app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
