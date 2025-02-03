from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.models.request.prediction import PredictionRequest
from app.services.prediction import get_predictor

prediction_router = APIRouter()


@prediction_router.post('/predict')
def predict(request: PredictionRequest, predictor=Depends(get_predictor)) -> JSONResponse:
    result = predictor.get_prediction(request)
    return jsonable_encoder(result)
