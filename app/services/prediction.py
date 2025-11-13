import pandas as pd
from io import StringIO
from pandas import DataFrame
from app.configuration.config import PgSqlSettings
from app.models.nixtla_models import PredictionRequest, PredictionResponse
from app.predictors.base import PredictorBase
from app.predictors.last_known_value import PredictorLastKnownValue
from app.repositories.persistent_models import PersistentModelsRepository

class PredictorFactory:
    def __init__(self, sql_config: PgSqlSettings) -> None:
        self._sql_config = sql_config
        self._models_repo = PersistentModelsRepository(sql_config)

    def create_predictor(self, request: PredictionRequest) -> PredictorBase:
        df = pd.read_csv(StringIO(request.csv))
        df = self._prepare_df(df)
        if request.model_type == "LastKnownValue":
            return self._create_last_known_value_predictor(df)
        else:
            raise ValueError(f'Predictor type {request.model_type} is not supported')

    @staticmethod
    def _prepare_df(df: DataFrame) -> DataFrame:
        df["date_str"] = df["<DATE>"].apply(lambda x: str(x).zfill(6)).astype(str)
        df["time_str"] = df["<TIME>"].apply(lambda x: str(x).zfill(6)).astype(str)
        df["datetime_str"] = df["date_str"] + df["time_str"]
        df["time_utc"] = pd.to_datetime(df["datetime_str"], format='%y%m%d%H%M%S', utc=True)
        df = df.set_index("time_utc")
        df.drop(["date_str", "time_str", "datetime_str", "<DATE>", "<TIME>"], axis=1, inplace=True)
        df.rename(columns={"<OPEN>": "open", "<HIGH>": "high", "<LOW>": "low", "<CLOSE>": "close", "<VOL>": "volume"},
                  inplace=True)
        return df

    @staticmethod
    def _create_last_known_value_predictor(df: DataFrame) -> PredictorBase:
        # last_model = self._models_repo.get_model_by_algo_name(algo)
        # fio = io.BytesIO(last_model.content)
        # model = ALGOS[last_model.algo].load(fio)
        return PredictorLastKnownValue(df)


class PredictionService:
    def __init__(self, sql_config: PgSqlSettings) -> None:
        self._sql_config = sql_config

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        predictor_factory = PredictorFactory(self._sql_config)
        predictor = predictor_factory.create_predictor(request)
        res = predictor.predict()
        return PredictionResponse(result=res)


