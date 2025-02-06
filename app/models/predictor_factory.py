import io
from enum import Enum
from typing import Dict, Type

import pandas as pd
from sb3_contrib import ARS, QRDQN, TQC, TRPO, RecurrentPPO
from stable_baselines3 import A2C, DDPG, DQN, PPO, SAC, TD3
from stable_baselines3.common.base_class import BaseAlgorithm

from app.configuration.config import PgSqlSettings
from app.models.feature_composer import FeatureComposer
from app.models.gym_env_factory import GymEnvFactory
from app.models.predictor_base import PredictorBase, PredictorRandomWalk, PredictorTrendFollowing
from app.models.predictor_sb3 import PredictorSb3
from app.repositories.sb3_models import Sb3ModelsRepository

ALGOS: Dict[str, Type[BaseAlgorithm]] = {
    "a2c": A2C,
    "ddpg": DDPG,
    "dqn": DQN,
    "ppo": PPO,
    "sac": SAC,
    "td3": TD3,
    # SB3 Contrib,
    "ars": ARS,
    "qrdqn": QRDQN,
    "tqc": TQC,
    "trpo": TRPO,
    "ppo_lstm": RecurrentPPO,
}


class PredictorType(str, Enum):
    Sb3 = 'Sb3'
    RandomWalk = 'RandomWalk'
    TrendFollowing = 'TrendFollowing'


class PredictorFactory:
    def __init__(self,
                 sql_config: PgSqlSettings,
                 candles: pd.DataFrame
                 ) -> None:

        self._sql_config = sql_config
        self._models_repo = Sb3ModelsRepository(sql_config)
        self._candles = candles

        fk = FeatureComposer(fill_missing_values=True)
        self._df = fk.compose(self._candles)

    def create_predictor(self,
                         predictor_type: PredictorType,
                         sb3_algo: str | None = None) -> PredictorBase:
        if predictor_type == PredictorType.RandomWalk:
            return self._create_rw_predictor()
        elif predictor_type == PredictorType.TrendFollowing:
            return self._create_tf_predictor()
        elif predictor_type == PredictorType.Sb3:
            return self._create_sb3_predictor(algo=sb3_algo)
        else:
            raise ValueError(f'Predictor type {predictor_type} is not supported')

    def _create_sb3_predictor(self, algo: str) -> PredictorBase:
        if algo is None or algo not in ALGOS:
            raise ValueError(f'Sb3 predictor algo=[{algo}] is not supported.')
        env_factory = GymEnvFactory(self._df)
        env, _ = env_factory.create_env()
        last_model = self._models_repo.get_model_by_algo_name(algo)
        fio = io.BytesIO(last_model.content)
        model = ALGOS[last_model.algo].load(fio)
        return PredictorSb3(env, model)

    def _create_rw_predictor(self) -> PredictorBase:
        return PredictorRandomWalk(self._df, seed=None)

    def _create_tf_predictor(self) -> PredictorBase:
        return PredictorTrendFollowing(self._df, threshold=0.50)
