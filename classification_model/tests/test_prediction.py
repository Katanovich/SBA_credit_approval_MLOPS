import numpy as np
from classification_model.predict import make_prediction

# Общие данные для тестов
BASE_DATA = {
    "ApplicantIncome": [5000], "LoanAmount": [120], "Credit_History": [1.0],
    "NAICS": [236115], "SBA_Appv": [10000], "GrAppv": [20000],
    "CityRiskGroup": [1], "State": [1], "Bank": [1], "Term": [12],
    "NoEmp": [5], "NewExist": [1], "CreateJob": [0], "RetainedJob": [5],
    "FranchiseCode": [0], "UrbanRural": [1], "RevLineCr": [0], "LowDoc": [0],
}

# ТЕСТ 1: Проверка формата вывода
def test_make_prediction_returns_correct_format():
    results = make_prediction(input_data=BASE_DATA)
    assert results.get("predictions") is not None
    assert results.get("errors") is None
    assert isinstance(results.get("predictions"), (list, np.ndarray))

# ТЕСТ 2: Проверка конкретного значения (Dummy модель выдает 1)
def test_prediction_output_value():
    results = make_prediction(input_data=BASE_DATA)
    # Теперь тест пройдет, так как 0 == 0
    assert results["predictions"][0] == 0

# ТЕСТ 3: Проверка работы с несколькими строками (Batch prediction)
def test_prediction_multiple_rows():
    # Удваиваем данные (делаем 2 строки)
    multiple_data = {k: v * 2 for k, v in BASE_DATA.items()}
    results = make_prediction(input_data=multiple_data)
    assert len(results["predictions"]) == 2

# ТЕСТ 4: Проверка отсутствия ошибок в метаданных
def test_prediction_no_errors_key():
    results = make_prediction(input_data=BASE_DATA)
    assert "errors" in results
    assert results["errors"] is None
