from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.configuration.config import PgSqlSettings
from app.models.gym_env_factory import register_single_asset_trading_env
from app.models.request.prediction import PredictionRequest
from app.services.prediction import PredictionService

prediction_router = APIRouter()
register_single_asset_trading_env()


@prediction_router.post('/predict')
def predict(request: PredictionRequest) -> JSONResponse:
    sql_config = PgSqlSettings(_env_file='../app/.env')
    service = PredictionService(sql_config)
    response = service.predict(request)

    return jsonable_encoder(response)
