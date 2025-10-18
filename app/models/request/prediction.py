from pydantic import BaseModel

class PredictionRequest(BaseModel):
    model_type: str
    content: str | None
    content_type: str | None

class PredictionResponse(BaseModel):
    content: str | None
    content_type: str | None


