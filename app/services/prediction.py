import abc
from datetime import datetime, timezone
from enum import Enum
from random import Random
from typing import List

from app.configuration.config import PgSqlSettings
from app.models.gym_env_single_asset import Action
from app.models.request.prediction import PredictionRequest, PredictionResult, PredictionItem
from app.repositories.tinvest_candles import TinvestCandlesRepository


class StrategyType(str, Enum):
    Sb3 = 'Sb3'
    RandomWalk = 'RandomWalk'
    TrendFollowing = 'TrendFollowing'


def get_predictor(request: PredictionRequest):
    if request.strategy == StrategyType.RandomWalk:
        return RandomWalkPredictor()
    elif request.strategy == StrategyType.TrendFollowing:
        return TrendFollowingPredictor()
    elif request.strategy == StrategyType.Sb3:
        return Sb3Predictor()
    else:
        return None


