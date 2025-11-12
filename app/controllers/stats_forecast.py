from datetime import datetime
from typing import List, Any

import numpy as np
import pandas as pd
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, HistoricAverage, Naive, RandomWalkWithDrift, GARCH

from app.models.prediction import Candle, PredictionResult

stats_forecast_router = APIRouter()

@stats_forecast_router.post('/random-walk-with-drift')
def random_walk_with_drift(request: List[Candle]) -> JSONResponse:
    forecast_df = stats_predict(request, RandomWalkWithDrift())
    return to_result(forecast_df.iloc[0]['RWD'], request[-1].time_utc)

@stats_forecast_router.post('/auto-arima')
def auto_arima(request: List[Candle]) -> JSONResponse:
    forecast_df = stats_predict(request, AutoARIMA())
    return to_result(forecast_df.iloc[0]['AutoARIMA'], request[-1].time_utc)

@stats_forecast_router.post('/garch')
def garch(request: List[Candle]) -> JSONResponse:
    forecast_df = stats_predict(request, GARCH())
    # TODO: Fix it
    return to_result(forecast_df.iloc[0]['GARCH(1,1)'], request[-1].time_utc)

@stats_forecast_router.post('/historic-average')
def historic_average(request: List[Candle]) -> JSONResponse:
    forecast_df = stats_predict(request, HistoricAverage())
    return to_result(forecast_df.iloc[0]['HistoricAverage'], request[-1].time_utc)

@stats_forecast_router.post('/naive')
def naive(request: List[Candle]) -> JSONResponse:
    forecast_df = stats_predict(request, Naive())
    return to_result(forecast_df.iloc[0]['Naive'], request[-1].time_utc)

def stats_predict(candles: List[Candle], model) -> pd.DataFrame:
    df = prepare_df(candles)
    sf = StatsForecast(models=[model], freq='min')
    sf.fit(df=df, time_col='time_utc', target_col='close')
    forecast_df = sf.predict(h=1)
    return forecast_df

def prepare_df(candles: List[Candle]) -> pd.DataFrame:
    data_for_df = [vars(candle) for candle in candles]
    df = pd.DataFrame(data_for_df)
    df['unique_id'] = 'candle'
    df.drop(['open', 'high', 'low', 'volume'], axis=1, inplace=True)
    return df

def to_result(price: float | None, time : datetime) -> Any:
    if np.isnan(price):
        price = None
    result = PredictionResult(predicted_price=price, time_utc=time, signal= None)
    return jsonable_encoder(result)
