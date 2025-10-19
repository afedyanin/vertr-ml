import abc
import pandas as pd
from io import StringIO
from pandas import DataFrame
from app.configuration.config import PgSqlSettings
from app.controllers.prediction import PredictionRequest, PredictionResponse
from app.repositories.persistent_models import PersistentModelsRepository


class PredictorBase(abc.ABC):
    def __init__(self, df: DataFrame) -> None:
        self._df = df

    def predict(self) -> DataFrame:
        pass


class PredictorDummy(PredictorBase):
    def __init__(self, df: DataFrame) -> None:
        super().__init__(df)

    def predict(self) -> DataFrame:
        return self._df


class PredictorFactory:
    def __init__(self, sql_config: PgSqlSettings) -> None:
        self._sql_config = sql_config
        self._models_repo = PersistentModelsRepository(sql_config)

    def create_predictor(self, request: PredictionRequest) -> PredictorBase:
        df = pd.read_csv(StringIO(request.csv))
        if request.model_type == "Dummy":
            return self._create_dummy_predictor(df)
        else:
            raise ValueError(f'Predictor type {request.model_type} is not supported')

    @staticmethod
    def _create_dummy_predictor(df: DataFrame) -> PredictorBase:
        # last_model = self._models_repo.get_model_by_algo_name(algo)
        # fio = io.BytesIO(last_model.content)
        # model = ALGOS[last_model.algo].load(fio)
        return PredictorDummy(df)


class PredictionService:
    def __init__(self, sql_config: PgSqlSettings) -> None:
        self._sql_config = sql_config

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        predictor_factory = PredictorFactory(self._sql_config)
        predictor = predictor_factory.create_predictor(request)
        df = predictor.predict()
        csv = df.to_csv(index=False)
        return PredictionResponse(csv=csv)


