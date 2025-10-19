import abc
from pandas import DataFrame

class PredictorBase(abc.ABC):
    def __init__(self, df: DataFrame) -> None:
        self._df = df

    def predict(self) -> DataFrame:
        pass


