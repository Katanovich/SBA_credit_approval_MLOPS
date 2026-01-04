from typing import Any, List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from classification_model.config.core import config
from classification_model.processing.data_manager import pre_pipeline_preparation


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    pre_processed = pre_pipeline_preparation(dataframe=input_data)

    validated_data = pre_processed[config.model_config.features].copy()
    errors = None

    try:
        MultipleSBADataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class SBADataInputSchema(BaseModel):
    City: Optional[str]
    SBA_Appv: Optional[float]
    ApprovalDate: Optional[Any]
    State: Optional[str]
    Bank: Optional[str]
    RevLineCr: Optional[str]
    LowDoc: Optional[str]
    NAICS: Optional[int]
    Term: Optional[int]
    NoEmp: Optional[int]
    NewExist: Optional[float]
    CreateJob: Optional[int]
    RetainedJob: Optional[int]
    FranchiseCode: Optional[int]
    UrbanRural: Optional[int]
    GrAppv: Optional[float]
    CityRiskGroup: Optional[str]
    Bankrisk: Optional[float]
    SBA_ratio: Optional[float]


class MultipleSBADataInputs(BaseModel):
    inputs: List[SBADataInputSchema]
