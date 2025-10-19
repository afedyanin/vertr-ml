from typing import Dict
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    model_type: str
    csv: str | None

class PredictionResponse(BaseModel):
    result: Dict | None
