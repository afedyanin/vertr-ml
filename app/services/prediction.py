import abc
from datetime import datetime, timezone
from random import Random
from typing import List

from app.models.data.prediction import StrategyType, Action
from app.models.request.prediction import PredictionReq, PredictionResult, PredictionItem


def get_predictor(request: PredictionReq):
    if request.strategy == StrategyType.RandomWalk:
        return RandomWalkPredictor()
    elif request.strategy == StrategyType.TrendFollowing:
        return TrendFollowingPredictor()
    elif request.strategy == StrategyType.Sb3:
        return Sb3Predictor()
    else:
        return None


class PredictorBase(abc.ABC):

    def __init__(self) -> None:
        self._rng = Random()

    def get_prediction(self, request: PredictionReq) -> PredictionResult:
        pass

    def _get_items(self) -> List[PredictionItem]:
        items = []
        for i in range(10):
            item = PredictionItem(
                time=datetime.now(timezone.utc),
                open=100.24,
                close=100.24,
                high=100.24,
                low=100.24,
                volume=223,
                is_completed = True,
                action = self._get_action()
            )
            items.append(item)
        return items

    def _get_action(self) -> Action:
        direction = self._rng.randint(-1, 1)
        if direction == 0:
            return Action.Hold
        if direction == 1:
            return Action.Buy
        if direction == -1:
            return Action.Sell


class RandomWalkPredictor(PredictorBase):

    def __init__(self) -> None:
        super().__init__()

    def get_prediction(self, request: PredictionReq) -> PredictionResult:
        result = PredictionResult(
            strategy=request.strategy,
            algo=request.algo,
            symbol=request.symbol,
            interval=request.interval,
            items=self._get_items()
        )
        return result


class TrendFollowingPredictor(PredictorBase):

    def __init__(self) -> None:
        super().__init__()

    def get_prediction(self, request: PredictionReq) -> PredictionResult:
        result = PredictionResult(
            strategy=request.strategy,
            algo=request.algo,
            symbol=request.symbol,
            interval=request.interval,
            items=self._get_items()
        )
        return result

    def _get_action(self) -> Action:
        return Action.Hold


class Sb3Predictor(PredictorBase):

    def __init__(self) -> None:
        super().__init__()

    def get_prediction(self, request: PredictionReq) -> PredictionResult:
        result = PredictionResult(
            strategy=request.strategy,
            algo=request.algo,
            symbol=request.symbol,
            interval=request.interval,
            items=self._get_items()
        )
        return result

    def _get_action(self) -> Action:
        return Action.Buy
