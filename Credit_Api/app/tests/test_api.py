import math
import numpy as np
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_make_prediction(sample_input_data):
    # Given
    payload = {
        "inputs": sample_input_data.to_dict(orient="records")
    }

    # When
    response = client.post(
        "http://localhost:8000/predict",
        json=payload,
    )

    # Then
    assert response.status_code == 200
    prediction_data = response.json()
    assert prediction_data["predictions"]
    assert prediction_data["errors"] is None
    assert isinstance(prediction_data["predictions"][0], (int, float))
