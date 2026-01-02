import numpy as np
from classification_model.predict import make_prediction


def test_make_prediction_returns_correct_format():
    # 1. Подготовка тестовых данных (пример)
    test_data = {
        "ApplicantIncome": 5000,
        "LoanAmount": 120,
        "Credit_History": 1.0,
        # добавь остальные поля, которые требует твоя модель
    }

    # 2. Вызов функции предсказания
    results = make_prediction(input_data=test_data)

    # 3. Проверки (Assertions)
    assert results.get("predictions") is not None
    assert isinstance(results.get("predictions"), (list, np.ndarray))
    assert results.get("errors") is None