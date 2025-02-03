import decimal

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Candle:
    time_utc: datetime
    interval: int
    symbol: str
    open: decimal
    close: decimal
    high: decimal
    low: decimal
    volume: decimal
    is_completed: bool
    candle_source: int

    @staticmethod
    def from_dict(candle: dict[str, Any]) -> "Candle":
        return Candle(
            time_utc=candle["time_utc"],
            interval=candle["interval"],
            symbol=candle["symbol"],
            open=candle["open"],
            close=candle["close"],
            high=candle["high"],
            low=candle["low"],
            volume=candle["volume"],
            is_completed=candle["is_completed"],
            candle_source=candle["candle_source"])
