from classification_model.predict import make_prediction


def test_make_prediction_basic(sample_input_data):
    # sample_input_data нужно подготовить или загрузить через load_dataset
    result = make_prediction(input_data=sample_input_data)

    assert result["predictions"] is not None
    assert not result["errors"]
