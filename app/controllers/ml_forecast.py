from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from mlforecast import MLForecast
from mlforecast.target_transforms import Differences

from app.models.nixtla_models import ForecastRequest, series_to_df, keys_to_stats_models, df_to_forecast_items, \
    mlforecast_all_models, keys_to_ml_models

'''
https://nixtlaverse.nixtla.io/statsforecast/src/core/models.html
'''
ml_forecast_router = APIRouter()

@ml_forecast_router.post('')
def forecast(request: ForecastRequest) -> JSONResponse:
    df = series_to_df(request.series)
    models = keys_to_ml_models(request.models)
    mlf = MLForecast(
        models=models,
        freq='min',
        lags=[1],
        target_transforms=[Differences([1])],
    )
    mlf.fit(df=df)
    forecast_df = mlf.predict(h=1)
    items = df_to_forecast_items(forecast_df, request.models)
    return jsonable_encoder(items)

@ml_forecast_router.get('/all-keys')
def get_all_keys() -> JSONResponse:
    return jsonable_encoder(mlforecast_all_models)

