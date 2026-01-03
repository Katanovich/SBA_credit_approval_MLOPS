# 🏦 SBA Loan Approval Prediction API

Production-ready ML service for predicting loan defaults based on SBA (Small Business Administration) data.

## 🛠 Tech Stack
- **Model:** XGBoost Classifier
- **API Framework:** FastAPI
- **CI/CD:** CircleCI
- **Containerization:** Docker
- **Environment:** Python 3.10-slim

## 🚀 Getting Started

### Using Docker (Recommended)
```bash
docker build -t sba-loan-api .
docker run -p 8001:8001 sba-loan-api

Manual Installation
Bash

pip install -r Credit_Api/requirements.txt
export PYTHONPATH=$PYTHONPATH:./Credit_Api
uvicorn Credit_Api.app.main:app --host 0.0.0.0 --port 8001
🧪 Testing & CI/CD
Automated tests are handled by CircleCI. Each commit triggers:

Environment setup.

Dependency installation.

Unit testing for model logic.

Docker image build verification.

📊 API Documentation
Once running, access the interactive Swagger UI at: http://localhost:8001/docs