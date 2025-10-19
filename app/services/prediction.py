from app.configuration.config import PgSqlSettings
from app.models.predictor_factory import PredictorFactory
from app.models.request.prediction import PredictionRequest, PredictionResponse

class PredictionService:
    def __init__(self, sql_config: PgSqlSettings) -> None:
        self._sql_config = sql_config

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        predictor_factory = PredictorFactory(self._sql_config)
        predictor = predictor_factory.create_predictor(request)
        df = predictor.predict()
        json = df.to_json(orient='split')
        return PredictionResponse(df_json=json)
