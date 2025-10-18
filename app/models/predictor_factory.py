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
        if request.model_type == "Dummy":
            return self._create_dummy_predictor(request.content, request.content_type)
        else:
            raise ValueError(f'Predictor type {request.model_type} is not supported')

    @staticmethod
    def _create_dummy_predictor(content: str, content_type: str) -> PredictorBase:
        # last_model = self._models_repo.get_model_by_algo_name(algo)
        # fio = io.BytesIO(last_model.content)
        # model = ALGOS[last_model.algo].load(fio)
        return PredictorDummy(content, content_type)
