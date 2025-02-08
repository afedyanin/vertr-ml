
from datetime import datetime, timezone

import psycopg2 as psycopg
import pandas as pd

from app.configuration.config import PgSqlSettings
from app.repositories.tinvest_candles import CandlesRepositoryBase


class SyntheticCandlesRepository(CandlesRepositoryBase):
    def __init__(self, config: PgSqlSettings):
        super().__init__(config)
        self._candles_table = "synthetic_candles"

    def get_candles(self,
                    symbol: str,
                    interval: int,
                    start_date_utc: datetime | None = None,
                    end_date_utc: datetime | None = None) -> pd.DataFrame:

        if start_date_utc is None:
            start_date_utc = datetime(2025, 1, 1, tzinfo=timezone.utc)

        if end_date_utc is None:
            end_date_utc = datetime.now(timezone.utc)

        sql = (f"SELECT * FROM {self._candles_table} "
               f"WHERE time_utc >= '{start_date_utc}' AND time_utc <= '{end_date_utc}' "
               f"AND symbol = '{symbol}' "
               f"AND interval = '{interval}'"
               )

        df = pd.read_sql_query(sql, self._engine)
        return df

    def get_last_candles(self,
                         symbol: str,
                         interval: int,
                         count: int = 10,
                         completed_only: bool = True) -> pd.DataFrame:

        if completed_only:
            completed_only_sql = f"AND is_completed = true"
        else:
            completed_only_sql = f""

        sql = (f"SELECT * FROM {self._candles_table} "
               f"WHERE symbol = '{symbol}' "
               f"AND interval = '{interval}' "
               f"{completed_only_sql} "
               f"ORDER BY time_utc DESC LIMIT {count} "
               )

        df = pd.read_sql_query(sql, self._engine)
        return df

    def insert_candles(self,
                       symbol: str,
                       interval: int,
                       candles: pd.DataFrame) -> int:
        with psycopg.connect(
                dbname=self._config.dbname,
                user=self._config.user,
                password=self._config.password,
                host=self._config.host,
                port=self._config.port) as conn:
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
                            row['is_complete'],
                            row['candle_source'],
                        ))
                    count = count + cur.rowcount
                conn.commit()

                return count
