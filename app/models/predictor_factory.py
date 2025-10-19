from io import StringIO

import pandas as pd
from pandas import DataFrame

from app.configuration.config import PgSqlSettings
from app.models.predictor_dummy import PredictorDummy
from app.models.request.prediction import PredictionRequest
from app.models.predictor_base import PredictorBase
from app.repositories.persistent_models import PersistentModelsRepository

class PredictorFactory:
    def __init__(self, sql_config: PgSqlSettings) -> None:
        self._sql_config = sql_config
        self._models_repo = PersistentModelsRepository(sql_config)

    def create_predictor(self, request: PredictionRequest) -> PredictorBase:
        df = pd.read_json(StringIO(request.df_json), orient='split')
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
