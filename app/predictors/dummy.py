from datetime import datetime, timezone
from typing import Dict
from pandas import DataFrame

from app.predictors.base import PredictorBase


class PredictorDummy(PredictorBase):
    def __init__(self, df: DataFrame) -> None:
        super().__init__(df)

    def predict(self) -> Dict:
        res = self._df.iloc[-1]["close"]

        result = {
            "next" : res.item(),
            "timestamp" : datetime.now(tz=timezone.utc),
        }

        return result
