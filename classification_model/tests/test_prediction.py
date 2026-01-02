import numpy as np
from classification_model.predict import make_prediction


def test_make_prediction_returns_correct_format():
    # 1. Подготовка тестовых данных
    # Добавляем все основные поля, чтобы препроцессинг не падал
    test_data = {
        "ApplicantIncome": [5000],
        "LoanAmount": [120],
        "Credit_History": [1.0],
        "NAICS": [236115],
        "SBA_Appv": [10000],  # Добавили
        "GrAppv": [20000],  # Добавили (часто идет в паре с SBA_Appv)
        "CityRiskGroup": [1],  # Видно в логах, что колонка существует в индексе
        # Если появятся новые KeyError, просто допишем их сюда
    }

    # 2. Вызов функции предсказания
    results = make_prediction(input_data=test_data)

    # 3. Проверки
    assert results.get("predictions") is not None
    assert results.get("errors") is None
    assert results["predictions"][0] == 1
    