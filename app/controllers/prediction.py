from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.models.request.prediction import PredictionReq
from app.services.prediction import get_predictor

prediction_router = APIRouter()


@prediction_router.post('/predict')
def predict(request: PredictionReq) -> JSONResponse:
    predictor = get_predictor(strategy_type=request.strategy)
    if predictor is None:
        return JSONResponse(content={'message': 'unknown strategy'}, status_code=500)

    result = predictor.get_prediction(request)
    return jsonable_encoder(result)
