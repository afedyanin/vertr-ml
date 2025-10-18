import abc

import pandas as pd

class PredictorBase(abc.ABC):
    def __init__(self, content: str | None, content_type: str | None) -> None:
        self._content = content
        self._content_type = content_type

    def predict(self) -> tuple:
        result = ""
        result_type = ""

        return result, result_type


