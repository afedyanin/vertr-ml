import abc
import decimal
from random import Random

import pandas as pd

from app.models.gym_env_single_asset import Action


class PredictorBase(abc.ABC):
    def __init__(self) -> None:
        pass

    def predict_last(self) -> tuple:
        time_index, predicted_actions = self._predict()
        return time_index[-1], predicted_actions[-1]

    def predict_all(self) -> pd.DataFrame:
        time_index, predicted_actions = self._predict()
        df_pred = pd.DataFrame(
            index=time_index,
            data={"action": predicted_actions},
        )
        return df_pred

    def _predict(self) -> tuple:
        time_index = []
        predicted_actions = []

        return time_index, predicted_actions


class PredictorRandomWalk(PredictorBase):
    def __init__(self, candles: pd.DataFrame, seed: int | None = None) -> None:
        super().__init__()
        self.candles = candles
        self._rng = Random(seed)

    def _predict(self) -> tuple:
        time_index = []
        predicted_actions = []
        for index, row in self.candles.iterrows():
            time_index.append(index)
            predicted_actions.append(self._rng.randint(Action.Hold.value, Action.Buy.value))

        return time_index, predicted_actions


class PredictorTrendFollowing(PredictorBase):

    def __init__(self, candles: pd.DataFrame, threshold: decimal = 0.01) -> None:
        super().__init__()
        self.candles = candles
        self.threshold = threshold

    def _predict(self) -> tuple:
        time_index = []
        predicted_actions = []
        for index, row in self.candles.iterrows():
            time_index.append(index)
            open_price = self.candles.loc[index, 'open']
            close_price = self.candles.loc[index, 'close']
            delta = close_price - open_price

            if abs(delta) < self.threshold:
                predicted_actions.append(Action.Hold.value)
            elif delta > 0:
                predicted_actions.append(Action.Buy.value)
            else:
                predicted_actions.append(Action.Sell.value)

        return time_index, predicted_actions

