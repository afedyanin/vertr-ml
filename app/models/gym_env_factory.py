from typing import Dict, Any

import pandas as pd
import gymnasium as gym

from huggingface_sb3 import EnvironmentName
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecEnv

from app.models.gym_env_single_asset import SingleAssetTrading


def register_single_asset_trading_env(version=1):
    name = 'SingleAssetTrading'
    last_version = gym.envs.registration.find_highest_version(ns=None, name=name)
    env_id = gym.envs.registration.get_env_id(ns=None, name=name, version=version)
    if last_version is None:
        gym.envs.registration.register(
            id=env_id,
            entry_point='app.models.gym_env_single_asset:SingleAssetTrading',
            disable_env_checker=True
        )
        spec = gym.spec(env_id)
        print(f"Environment registered. {spec}")


class GymEnvFactory:
    def __init__(
            self,
            composed_df: pd.DataFrame,
            env_id: str = "SingleAssetTrading-v1"):

        self.env_name = EnvironmentName(env_id)
        self.composed_df = composed_df

    def create_vector_env(
            self,
            episode_duration: int | str = "max") -> (VecEnv, int):

        env_kwargs, episode_steps = self._compose_kwargs(episode_duration=episode_duration)

        env = make_vec_env(
            self.env_name.gym_id,
            n_envs=1,
            env_kwargs=env_kwargs,
            monitor_dir=None)

        return env, episode_steps

    def create_env(
            self,
            episode_duration: int | str = "max") -> (gym.Env, int):

        env_kwargs, episode_steps = self._compose_kwargs(episode_duration=episode_duration)

        spec = gym.spec(self.env_name.gym_id)
        env = spec.make(**env_kwargs)

        return env, episode_steps

    def _compose_kwargs(
            self,
            episode_duration: int | str = "max") -> (Dict[str, Any], int):

        env_kwargs = {
            'df': self.composed_df,
            'max_episode_duration': episode_duration,
            'render_mode': 'ansi'
        }

        episode_steps = SingleAssetTrading.get_time_steps(self.composed_df, episode_duration)
        return env_kwargs, episode_steps



