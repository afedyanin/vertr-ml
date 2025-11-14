from datetime import datetime

import pandas as pd
import lightgbm as lgb
from pydantic import BaseModel
from statsforecast.models import Naive, AutoARIMA, HistoricAverage, RandomWalkWithDrift, AutoETS, AutoCES, AutoTheta

from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor


# https://nixtlaverse.nixtla.io/

class SeriesItem(BaseModel):
    unique_id: str
    ds: datetime
    y: float

class ForecastItem(BaseModel):
    model: str
    unique_id: str | None
    ds : datetime | None
    value: float | None

class ForecastRequest(BaseModel):
    models: list[str]
    series: list[SeriesItem]

def series_to_df(series: list[SeriesItem]) -> pd.DataFrame:
    data_for_df = [vars(item) for item in series]
    df = pd.DataFrame(data_for_df)
    return df

def df_to_forecast_items(df: pd.DataFrame, model_keys: list[str]) -> list[ForecastItem]:
    items = []
    for index, row in df.iterrows():
        for key in model_keys:
            if key in df.columns:
                fi = ForecastItem(model=key, ds=row['ds'], unique_id=row['unique_id'], value=row[key])
                items.append(fi)
    return items

## statsforecast

statsforecast_all_models = [
    'naive',
    'auto_arima',
    'auto_ets',
    'auto_ces',
    'auto_theta',
    'random_walk',
    'history_average',
]

def keys_to_stats_models(model_keys: list[str]) -> list:
    stats_models = []
    for model_key in model_keys:
        stats_models.append(_get_stats_model_by_key(model_key))
    return stats_models

def _get_stats_model_by_key(model_key: str):
    match model_key:
        case 'naive':
            return Naive(alias=model_key)
        case 'auto_arima':
            return AutoARIMA(alias=model_key)
        case 'auto_ets':
            return AutoETS(alias=model_key)
        case 'auto_ces':
            return AutoCES(alias=model_key)
        case 'auto_theta':
            return AutoTheta(alias=model_key)
        case 'random_walk':
            return RandomWalkWithDrift(alias=model_key)
        case 'history_average':
            return HistoricAverage(alias=model_key)
        case _:
            return None


## ml_forecast

mlforecast_all_models = [
    'lgbm',
    'lasso',
    'lin_reg',
    'ridge',
    'knn',
    'mlp',
    'rf',
]

def keys_to_ml_models(model_keys: list[str]) -> dict:
    ml_models = {}
    for model_key in model_keys:
        model = _get_ml_model_by_key(model_key)
        if model is None:
            continue
        ml_models[model_key] = model
    return ml_models

def _get_ml_model_by_key(model_key: str):
    match model_key:
        case 'lgbm':
            return lgb.LGBMRegressor(verbosity=-1)
        case 'lasso':
            return Lasso()
        case 'lin_reg':
            return LinearRegression()
        case 'ridge':
            return Ridge()
        case 'knn':
            return KNeighborsRegressor()
        case 'mlp':
            return MLPRegressor()
        case 'rf':
            return RandomForestRegressor()
        case _:
            return None
