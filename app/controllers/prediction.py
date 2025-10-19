from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.configuration.config import PgSqlSettings
from app.services.prediction import PredictionService

class PredictionRequest(BaseModel):
    model_type: str
    csv: str | None

class PredictionResponse(BaseModel):
    csv: str | None

prediction_router = APIRouter()

@prediction_router.post('/predict')
def predict(request: PredictionRequest) -> JSONResponse:
    sql_config = PgSqlSettings(_env_file='../app/.env')
    service = PredictionService(sql_config)
    response = service.predict(request)

    return jsonable_encoder(response)

