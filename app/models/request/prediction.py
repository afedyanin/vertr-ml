from pydantic import BaseModel
from app.models.data.prediction import StrategyType


class PredictionReq(BaseModel):
    strategy: StrategyType
    algo: str
    symbol: str
    interval: str
    steps: int


class PredictionResult(BaseModel):
    strategy: StrategyType
    algo: str
    symbol: str
    interval: str
    action: int
