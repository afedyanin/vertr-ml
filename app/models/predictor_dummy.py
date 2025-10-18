from app.models.predictor_base import PredictorBase

class PredictorDummy(PredictorBase):
    def __init__(self, content: str | None, content_type: str | None) -> None:
        super().__init__(content, content_type)

    def predict(self) -> tuple:
        result = f"Dummy: request={self._content} content_type={self._content_type}"
        result_type = "string"

        return result, result_type

