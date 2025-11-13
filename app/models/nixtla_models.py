from datetime import datetime

import pandas as pd
from pydantic import BaseModel

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

class ForecastResult(BaseModel):
    forecasts: list[ForecastItem]

# TODO: Test me
def series_to_df(series: list[SeriesItem]) -> pd.DataFrame:
    df = pd.DataFrame(series)
    return df

# TODO: Implement me
def df_to_forecast_items(df: pd.DataFrame) -> list[ForecastItem]:
    return []