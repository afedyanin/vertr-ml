from pandas import DataFrame

from app.models.predictor_base import PredictorBase

class PredictorDummy(PredictorBase):
    def __init__(self, df: DataFrame) -> None:
        super().__init__(df)

    def predict(self) -> DataFrame:
        return self._df

