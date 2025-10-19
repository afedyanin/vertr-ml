from pydantic import BaseModel

class PredictionRequest(BaseModel):
    model_type: str
    df_json: str | None

class PredictionResponse(BaseModel):
    df_json: str | None


