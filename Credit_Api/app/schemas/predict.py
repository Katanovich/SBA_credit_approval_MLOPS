from typing import Any, List, Optional
from pydantic import BaseModel
from classification_model.processing.validation import SBADataInputSchema

class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[int]]

class MultipleSBADataInputs(BaseModel):
    inputs: List[SBADataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "City": "CHATTANOOGA",
                        "State": "TN",
                        "Zip": 37421,
                        "Bank": "SOUTH EAST BANK, N.A.",
                        "BankState": "TN",
                        "NAICS": 453210,
                        "ApprovalDate": "7-Feb-06",
                        "ApprovalFY": 2006,
                        "Term": 240,
                        "NoEmp": 2,
                        "NewExist": 1,
                        "CreateJob": 0,
                        "RetainedJob": 2,
                        "FranchiseCode": 1,
                        "UrbanRural": 1,
                        "RevLineCr": "N",
                        "LowDoc": "N",
                        "GrAppv": 480000,
                        "SBA_Appv": 360000,
                       # "MIS_Status": "P I F"
                    }
                ]
            }
        }
