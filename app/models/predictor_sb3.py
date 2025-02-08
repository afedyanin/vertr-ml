from gymnasium import Env
from stable_baselines3.common.base_class import BaseAlgorithm

from app.models.predictor_base import PredictorBase


class PredictorSb3(PredictorBase):
    def __init__(self, env: Env, model: BaseAlgorithm):
        super().__init__()
        self.env = env
        self.model = model

    def predict(self) -> tuple:
        observation, info = self.env.reset()
        is_done = False
        time_index = []
        predicted_actions = []

        while not is_done:
            action, _ = self.model.predict(observation=observation, deterministic=True)
            time_index.append(info["time_utc"])
            predicted_actions.append(action.item())

            observation, reward, terminated, truncated, info = self.env.step(action)
            is_done = terminated or truncated

        # выход из цикла вернул данные по последней свече
        # используем их для реального предсказания
        action, _ = self.model.predict(observation=observation, deterministic=True)
        time_index.append(info["time_utc"])
        predicted_actions.append(action.item())

        return time_index, predicted_actions

