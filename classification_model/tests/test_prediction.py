import numpy as np
import pandas as pd
from classification_model.predict import make_prediction


def test_make_prediction_returns_correct_format():

    test_data = {
        "ApplicantIncome": [5000],
        "LoanAmount": [120],
        "Credit_History": [1.0],
        "NAICS": [236115],
        "SBA_Appv": [10000],
        "GrAppv": [20000],
        "CityRiskGroup": [1],
        "State": [1],
        "Bank": [1],
        "Term": [12],
        "NoEmp": [5],
        "NewExist": [1],
        "CreateJob": [0],
        "RetainedJob": [5],
        "FranchiseCode": [0],
        "UrbanRural": [1],
        "RevLineCr": [0],
        "LowDoc": [0],
    }

    # 2. Вызов функции предсказания
    results = make_prediction(input_data=test_data)

    # 3. Проверки (Assertions)
    # Проверяем, что словарь результатов содержит предсказания и не содержит ошибок
    assert results.get("predictions") is not None
    assert results.get("errors") is None

    # Проверяем тип данных (должен быть список или массив numpy)
    assert isinstance(results.get("predictions"), (list, np.ndarray))

    # Проверяем конкретное значение (наша dummy-модель всегда возвращает 1)
    assert results["predictions"][0] == 1
