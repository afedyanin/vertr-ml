from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.models.data.candle import Interval
from app.models.gym_env_single_asset import Action
from app.models.predictor_factory import PredictorType


class PredictionRequest(BaseModel):
    symbol: str = "SBER"
    interval: int = Interval.CANDLE_INTERVAL_10_MIN.value
    predictor: str = PredictorType.Sb3.value
    algo: str = "dqn"
    candles_count: int = 20
    completed_candles_only: bool = True
    candles_source: str = "tinvest"


class PredictionResponse(BaseModel):
    time: List[datetime]
    action: List[Action]


