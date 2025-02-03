import decimal
from datetime import datetime
from typing import List

from pydantic import BaseModel
from app.models.data.prediction import StrategyType, Action


class PredictionRequest(BaseModel):
    strategy: StrategyType
    algo: str
    # источник данных: т-инвест, исс, синтетика и т.п.
    source: str
    symbol: str
    interval: str
    # количество свечей для предсказания, начиная с последней
    steps: int


class PredictionItem(BaseModel):
    # время начала свечи
    time: datetime
    open: decimal
    high: decimal
    low: decimal
    close: decimal
    # объём торгов в лотах.
    volume: int
    # признак завершения свечи
    is_completed: bool
    # предсказанное действие на основании данных из этой свечи
    action: Action


class PredictionResult(BaseModel):
    strategy: StrategyType
    algo: str
    symbol: str
    interval: str
    items: List[PredictionItem]


