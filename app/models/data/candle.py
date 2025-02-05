import decimal

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
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


class Interval(int, Enum):
    CANDLE_INTERVAL_UNSPECIFIED = 0
    CANDLE_INTERVAL_1_MIN = 1
    CANDLE_INTERVAL_2_MIN = 6
    CANDLE_INTERVAL_3_MIN = 7
    CANDLE_INTERVAL_5_MIN = 2
    CANDLE_INTERVAL_10_MIN = 8
    CANDLE_INTERVAL_15_MIN = 3
    CANDLE_INTERVAL_30_MIN = 9
    CANDLE_INTERVAL_HOUR = 4
    CANDLE_INTERVAL_2_HOUR = 10
    CANDLE_INTERVAL_4_HOUR = 11
    CANDLE_INTERVAL_DAY = 5
    CANDLE_INTERVAL_WEEK = 12
    CANDLE_INTERVAL_MONTH = 13

    def equal(self, interval: "Interval") -> bool:
        return self.value == interval.value
