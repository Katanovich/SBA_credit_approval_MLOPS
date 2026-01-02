from classification_model.predict import make_prediction


def test_make_prediction_returns_correct_format():
    # 1. Подготовка тестовых данных
    # Добавляем [], чтобы значения стали списками (1 строка данных)
    test_data = {
        "ApplicantIncome": [5000],
        "LoanAmount": [120],
        "Credit_History": [1.0],
    }

    # 2. Вызов функции предсказания
    results = make_prediction(input_data=test_data)

    # 3. Проверки
    assert results.get("predictions") is not None
    # Так как мы используем Dummy-модель, она вернет [1]
    assert results["predictions"][0] == 1