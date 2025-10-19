import pandas as pd
from pandas import DataFrame

from app.services.prediction import PredictorBase


class PredictorDummy(PredictorBase):
    def __init__(self, df: DataFrame) -> None:
        super().__init__(df)

    def predict(self) -> DataFrame:
        result = {
            "next" : self._df.iloc[-1]["close"]
        }
        df = pd.DataFrame(result)
        return df
