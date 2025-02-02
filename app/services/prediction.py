import abc
from random import Random

from app.models.data.prediction import StrategyType
from app.models.request.prediction import PredictionReq, PredictionResult


def get_predictor(strategy_type: StrategyType):
    if strategy_type == StrategyType.RandomWalk:
        return RandomWalkPredictor(seed=None)
    elif strategy_type == StrategyType.TrendFollowing:
        return TrendFollowingPredictor()
    elif strategy_type == StrategyType.Sb3:
        return Sb3Predictor()
    else:
        return None


class PredictorBase(abc.ABC):
    def get_prediction(self, request: PredictionReq) -> PredictionResult:
        pass


class RandomWalkPredictor(PredictorBase):

    def __init__(self, seed: int | None) -> None:
        if seed is None:
            self.random = Random()
        else:
            self.random = Random(seed)

    def get_prediction(self, request: PredictionReq) -> PredictionResult:
        result = PredictionResult(
            strategy=request.strategy,
            algo=request.algo,
            symbol=request.symbol,
            interval=request.interval,
            action=self.random.randint(1, 10)
        )
        return result


class TrendFollowingPredictor(PredictorBase):

    def __init__(self) -> None:
        pass

    def get_prediction(self, request: PredictionReq) -> PredictionResult:
        result = PredictionResult(
            strategy=request.strategy,
            algo=request.algo,
            symbol=request.symbol,
            interval=request.interval,
            action=5
        )
        return result


class Sb3Predictor(PredictorBase):

    def __init__(self) -> None:
        pass

    def get_prediction(self, request: PredictionReq) -> PredictionResult:
        result = PredictionResult(
            strategy=request.strategy,
            algo=request.algo,
            symbol=request.symbol,
            interval=request.interval,
            action=3
        )
        return result
