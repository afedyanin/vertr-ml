from pydantic import BaseModel


class PredictionRequest(BaseModel):
    model_type: str
    csv: str | None

class PredictionResponse(BaseModel):
    csv: str | None
