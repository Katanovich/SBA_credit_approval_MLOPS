import typing as t
import pandas as pd

from classification_model import __version__ as _version
from classification_model.config.core import config
from classification_model.processing.data_manager import load_pipeline
from classification_model.processing.validation import validate_inputs
# Импортируем напрямую из файла logger.py в этом же пакете
from classification_model.logger import get_logger

_logger = get_logger(__name__)

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
xgb = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
        *,
        input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)

    # Логируем вход
    _logger.info(f"Inputs: {input_data}")

    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = xgb.predict(X=validated_data[config.model_config.features])
        results = {
            "predictions": predictions.tolist() if hasattr(predictions, "tolist") else predictions,
            "version": _version,
            "errors": errors,
        }
        # Логируем успех
        _logger.info(f"Result: {results['predictions']}")
    else:
        # Логируем ошибку
        _logger.warning(f"Errors: {errors}")

    return results
