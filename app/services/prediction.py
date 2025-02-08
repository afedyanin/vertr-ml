from app.configuration.config import PgSqlSettings
from app.models.predictor_factory import PredictorFactory, PredictorType
from app.models.request.prediction import PredictionRequest, PredictionResponse
from app.repositories.synthetic_candles import SyntheticCandlesRepository
from app.repositories.tinvest_candles import TinvestCandlesRepository, CandlesRepositoryBase


class PredictionService:
    def __init__(self, sql_config: PgSqlSettings) -> None:
        self._sql_config = sql_config

    def predict(self, request: PredictionRequest) -> PredictionResponse:

        candles_repo = self._candles_repo_factory(request.candles_source)
        candles = candles_repo.get_last_candles(
            symbol=request.symbol,
            interval=request.interval,
            count=request.candles_count,
            completed_only=request.completed_candles_only)

        predictor_factory = PredictorFactory(self._sql_config, candles)
        predictor = predictor_factory.create_predictor(
            predictor_type=request.predictor,
            sb3_algo=request.algo)

        items_time, items_action = predictor.predict()
        return PredictionResponse(time=items_time, action=items_action)

    def _candles_repo_factory(self, candles_source: str) -> CandlesRepositoryBase:
        if candles_source == 'tinvest':
            return TinvestCandlesRepository(self._sql_config)
        if candles_source == 'synthetic':
            return SyntheticCandlesRepository(self._sql_config)
        raise ValueError(f'Invalid candles source: {candles_source}')
