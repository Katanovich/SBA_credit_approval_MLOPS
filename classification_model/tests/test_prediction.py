import numpy as np
from classification_model.predict import make_prediction


def test_make_prediction_returns_correct_format():
    # 1. Подготовка тестовых данных
    # Нужно передать ВСЕ колонки, которые модель использует в препроцессинге
    test_data = {
        "ApplicantIncome": [5000],
        "LoanAmount": [120],
        "Credit_History": [1.0],
        "NAICS": [236115],  # Добавили отсутствующее поле (пример кода NAICS)
        # Если модель потребует что-то еще, добавь по аналогии ниже
    }

    # 2. Вызов функции предсказания
    results = make_prediction(input_data=test_data)

    # 3. Проверки
    assert results.get("predictions") is not None
    assert results.get("errors") is None
    # Проверяем, что получили предсказание от нашей dummy-модели
    assert results["predictions"][0] == 1