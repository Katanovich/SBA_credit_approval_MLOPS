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
        "State": ["CA"],
        "Bank": ["CHASE"],
        "Term": [12],
        "NoEmp": [5],
        "NewExist": [1],
        "CreateJob": [0],
        "RetainedJob": [5],
        "FranchiseCode": [0],
        "UrbanRural": [1],
        "RevLineCr": ["N"],
        "LowDoc": ["N"],
    }


    results = make_prediction(input_data=test_data)


    assert results.get("predictions") is not None
    assert results.get("errors") is None
    assert results["predictions"][0] == 1
    