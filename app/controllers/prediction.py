from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.configuration.config import PgSqlSettings
from app.models.nixtla_models import PredictionRequest, Candle, PredictionResult
from app.services.prediction import PredictionService

prediction_router = APIRouter()

@prediction_router.post('/predict')
def predict(request: PredictionRequest) -> JSONResponse:
    sql_config = PgSqlSettings(_env_file='../app/.env')
    service = PredictionService(sql_config)
    response = service.predict(request)

    return jsonable_encoder(response)

