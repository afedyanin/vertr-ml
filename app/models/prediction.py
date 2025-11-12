from datetime import datetime
from typing import Dict
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    model_type: str
    csv: str | None

class PredictionResponse(BaseModel):
    result: Dict | None

class Candle (BaseModel):
    time_utc: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

class PredictionResult(BaseModel):
    time_utc: datetime | None
    predicted_price: float | None
    signal: int | None
