
from datetime import datetime, timezone, timedelta

import pandas as pd

from tinkoff.invest import Instrument, Client, InstrumentIdType, CandleInterval
from tinkoff.invest.schemas import CandleSource
from tinkoff.invest.utils import quotation_to_decimal

from app.configuration.config import TinvestSettings


class TinvestAdapter:
    def __init__(self, config: TinvestSettings):
        self._config = config

    def get_instrument(
            self,
            ticker: str = "SBER",
            class_code: str = "TQBR") -> Instrument:
        with Client(self._config.token) as client:
            response = client.instruments.get_instrument_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
                class_code=class_code,
                id=ticker)
            return response.instrument

    def find_instrument(self, query: str) -> list[Instrument]:
        with Client(self._config.token) as client:
            response = client.instruments.find_instrument(query=query)
            return response.instruments

    def get_candles(
            self,
            instrument_id: str,
            start_date_utc: datetime | None = None,
            end_date_utc: datetime | None = None,
            interval: CandleInterval = CandleInterval.CANDLE_INTERVAL_10_MIN) -> pd.DataFrame:

        if end_date_utc is None:
            end_date_utc = datetime.now(timezone.utc)

        if start_date_utc is None:
            start_date_utc = end_date_utc - timedelta(days=2)

        with Client(self._config.token) as client:
            candles = client.get_all_candles(
                instrument_id=instrument_id,
                from_=start_date_utc,
                to=end_date_utc,
                interval=interval,
                candle_source_type=CandleSource.CANDLE_SOURCE_EXCHANGE,
            )

            df = pd.DataFrame([{
                'time_utc': c.time,
                'open': pd.to_numeric(quotation_to_decimal(c.open)),
                'high': pd.to_numeric(quotation_to_decimal(c.high)),
                'low': pd.to_numeric(quotation_to_decimal(c.low)),
                'close': pd.to_numeric(quotation_to_decimal(c.close)),
                'volume': pd.to_numeric(c.volume),
                'is_complete': c.is_complete,
                'candle_source': c.candle_source_type,
            } for c in candles])

            return df
