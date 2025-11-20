from typing import Any

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from neuralforecast.auto import AutoLSTM, AutoRNN, AutoMLP, AutoDeepAR, AutoDeepNPTS, AutoKAN, AutoTFT, AutoTimesNet
from neuralforecast.common._base_auto import BaseAuto
from neuralforecast.tsdataset import TimeSeriesDataset
from starlette.responses import JSONResponse
import torch as torch

from app.models.nixtla_models import series_to_df, SeriesItem

neural_forecast_router = APIRouter()

@neural_forecast_router.post('/AutoLSTM')
def forecast(series: list[SeriesItem]) -> JSONResponse:
    ## TODO: move config in request params
    config = dict(max_steps=1, val_check_steps=1, input_size=5, encoder_hidden_size=8)
    model = AutoLSTM(h=1, config=config, num_samples=4)
    predicted_value = _forecast_by_model(series, model)
    return jsonable_encoder(predicted_value)

@neural_forecast_router.post('/AutoRNN')
def forecast(series: list[SeriesItem]) -> JSONResponse:
    config = dict(max_steps=1, val_check_steps=1, input_size=5, encoder_hidden_size=8)
    model = AutoRNN(h=1, config=config, num_samples=4)
    predicted_value = _forecast_by_model(series, model)
    return jsonable_encoder(predicted_value)

@neural_forecast_router.post('/AutoMLP')
def forecast(series: list[SeriesItem]) -> JSONResponse:
    config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
    model = AutoMLP(h=1, config=config, num_samples=4)
    predicted_value = _forecast_by_model(series, model)
    return jsonable_encoder(predicted_value)

@neural_forecast_router.post('/AutoDeepAR')
def forecast(series: list[SeriesItem]) -> JSONResponse:
    config = dict(max_steps=1, val_check_steps=1, input_size=12, lstm_hidden_size=8)
    model = AutoDeepAR(h=1, config=config, num_samples=4)
    predicted_value = _forecast_by_model(series, model)
    return jsonable_encoder(predicted_value)

@neural_forecast_router.post('/AutoDeepNPTS')
def forecast(series: list[SeriesItem]) -> JSONResponse:
    config = dict(max_steps=1, val_check_steps=1, input_size=12)
    model = AutoDeepNPTS(h=1, config=config, num_samples=4)
    predicted_value = _forecast_by_model(series, model)
    return jsonable_encoder(predicted_value)

@neural_forecast_router.post('/AutoKAN')
def forecast(series: list[SeriesItem]) -> JSONResponse:
    config = dict(max_steps=1, val_check_steps=1, input_size=12)
    model = AutoKAN(h=1, config=config, num_samples=4)
    predicted_value = _forecast_by_model(series, model)
    return jsonable_encoder(predicted_value)

@neural_forecast_router.post('/AutoTFT')
def forecast(series: list[SeriesItem]) -> JSONResponse:
    config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
    model = AutoTFT(h=1, config=config, num_samples=4)
    predicted_value = _forecast_by_model(series, model)
    return jsonable_encoder(predicted_value)

@neural_forecast_router.post('/AutoTimesNet')
def forecast(series: list[SeriesItem]) -> JSONResponse:
    config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=32)
    model = AutoTimesNet(h=1, config=config, num_samples=4)
    predicted_value = _forecast_by_model(series, model)
    return jsonable_encoder(predicted_value)

def _forecast_by_model(series: list[SeriesItem], model: BaseAuto) -> Any:
    df = series_to_df(series)
    dataset, *_ = TimeSeriesDataset.from_df(df)
    torch.set_float32_matmul_precision('high')
    model.fit(dataset=dataset)
    y_hat = model.predict(dataset=dataset)
    predicted_value = y_hat[0][0].item()
    return predicted_value
