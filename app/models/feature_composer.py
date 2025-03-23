from datetime import datetime
import pandas as pd

from app.models.data.candle import Interval


class FeatureComposer:

    def __init__(
            self,
            fill_missing_values: bool = True,
    ):
        self._fill_missing_values = fill_missing_values
        self._columns_to_drop = [
            'interval', 'symbol', 'high', 'low', 'value', 'volume', 'is_completed', 'candle_source']

    def compose(self, candles: pd.DataFrame) -> pd.DataFrame:
        interval = FeatureComposer._get_interval(candles)
        candles.drop(columns=self._columns_to_drop, inplace=True, errors='ignore')
        candles.set_index('time_utc', inplace=True)
        candles.sort_index(inplace=True)

        if self._fill_missing_values:
            candles = self._fill_missing(candles, interval)
            candles = self._interpolate(candles)

        candles = self._add_returns(candles)
        candles["info_intraday_return"] = (candles["close"] - candles["open"]).round(6)
        candles.dropna(inplace=True)

        return candles

    @staticmethod
    def _fill_missing(df: pd.DataFrame, interval: Interval) -> pd.DataFrame:
        freq = FeatureComposer._interval_to_frequency(interval)
        d_idx = pd.date_range(df.index.min(), df.index.max(), freq=freq)
        df = df.reindex(index=d_idx)
        return df

    @staticmethod
    def _get_interval(df: pd.DataFrame) -> Interval:
        interval = df.iloc[0]["interval"]
        return Interval(interval)

    @staticmethod
    def _interpolate(df: pd.DataFrame) -> pd.DataFrame:
        df.interpolate(axis=0, method='polynomial', order=3, limit_direction='both', inplace=True)
        return df

    @staticmethod
    def _add_returns(df: pd.DataFrame) -> pd.DataFrame:
        df["feature_close_return"] = (df["close"] - df["close"].shift(1)).round(6)
        df["feature_ret_m1"] = df["feature_close_return"].shift(1)
        df["feature_ret_m2"] = df["feature_close_return"].shift(2)
        df["feature_ret_m3"] = df["feature_close_return"].shift(3)
        return df

    @staticmethod
    def _add_values(df: pd.DataFrame) -> pd.DataFrame:
        df["feature_value_return"] = df["value"]#.pct_change(1)
        df["feature_val_m1"] = df["feature_value_return"].shift(1)
        return df


    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
    @staticmethod
    def _interval_to_frequency(interval: Interval) -> str:
        if interval.equal(Interval.CANDLE_INTERVAL_MONTH):
            return "1MS"
        if interval.equal(Interval.CANDLE_INTERVAL_WEEK):
            return "1W"
        if interval.equal(Interval.CANDLE_INTERVAL_DAY):
            return "1D"
        if interval.equal(Interval.CANDLE_INTERVAL_HOUR):
            return "1h"
        if interval.equal(Interval.CANDLE_INTERVAL_30_MIN):
            return "30min"
        if interval.equal(Interval.CANDLE_INTERVAL_15_MIN):
            return "15min"
        if interval.equal(Interval.CANDLE_INTERVAL_10_MIN):
            return "10min"
        if interval.equal(Interval.CANDLE_INTERVAL_5_MIN):
            return "5min"
        if interval.equal(Interval.CANDLE_INTERVAL_1_MIN):
            return "1min"

        raise ValueError(f"Interval {interval.name} not supported.")

