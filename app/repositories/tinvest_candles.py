import psycopg
import pandas as pd


class TinvestCandlesRepository:
    def __init__(self):
        self._candles_table = "tinvest_candles"

    def insert_candles(self, symbol: str, interval: int, candles: pd.DataFrame) -> int:
        """
        Вставить список свечей в БД
        """
        with (psycopg.connect()) as conn:
            with conn.cursor() as cur:
                count = 0
                for index, row in candles.iterrows():
                    cur.execute(
                        f"INSERT INTO {self._candles_table} ("
                        "time_utc, interval, symbol, open, high, low, close, volume, is_completed, candle_source)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                        "ON CONFLICT ON CONSTRAINT tinvest_candles_unique DO UPDATE "
                        "SET open = EXCLUDED.open, "
                        "close = EXCLUDED.close, "
                        "high = EXCLUDED.high, "
                        "low = EXCLUDED.low, "
                        "volume = EXCLUDED.volume, "
                        "is_completed = EXCLUDED.is_completed, "
                        "candle_source = EXCLUDED.candle_source ",
                        (
                            row['time_utc'],
                            interval,
                            symbol,
                            row['open'],
                            row['high'],
                            row['low'],
                            row['close'],
                            row['volume'],
                            row['is_completed'],
                            row['candle_source'],
                        ))
                    count = count + cur.rowcount
                conn.commit()

                return count
