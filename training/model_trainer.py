import sys
from typing import Dict, Type, Any

import gymnasium as gym
import pandas as pd
import torch as th

from sb3_contrib import ARS, QRDQN, TQC, TRPO, RecurrentPPO
from stable_baselines3 import A2C, DDPG, DQN, PPO, SAC, TD3
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

from app.models.feature_composer import FeatureComposer

sys.path.append("../app/models")

from app.models.gym_env_factory import GymEnvFactory
from training import hyperparams as hp

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


class ModelTrainer:
    def __init__(self,
                 algo: str,
                 verbose: int = 1,
                 device: th.device | str = "auto",
                 log_dir: str | None = None,
                 ):
        self.algo = algo
        self.verbose = verbose
        self.device = device
        self.log_dir = log_dir
        self._fk = FeatureComposer()

    def train(self,
              candles_df: pd.DataFrame,
              episode_duration: int | str = "max",
              episodes: int = 1000,
              hyperparams: Dict[str, Any] | None = None,
              optimized: bool = False,
              ) -> BaseAlgorithm:

        train_df = self._fk.compose(candles_df)
        env_factory = GymEnvFactory(train_df)
        training_env, episode_steps = env_factory.create_env(episode_duration=episode_duration)
        time_steps = episode_steps * episodes
        print(f"Training algo {self.algo}:  {time_steps} time steps.")

        model = self._train(
            env=training_env,
            time_steps=time_steps,
            hyperparams=hyperparams,
            optimized=optimized)

        return model

    def evaluate(self,
                 candles_df: pd.DataFrame,
                 model: BaseAlgorithm,
                 episode_duration: int | str = "max",
                 episodes: int = 1000,
                 return_episode_rewards: bool = False):

        eval_df = self._fk.compose(candles_df)
        env_factory = GymEnvFactory(eval_df)
        eval_env, _ = env_factory.create_env(episode_duration=episode_duration)

        return ModelTrainer._evaluate(
            env=eval_env,
            model=model,
            eval_episodes=episodes,
            return_episode_rewards=return_episode_rewards)

    def _train(
            self,
            env: gym.Env,
            time_steps: int,
            hyperparams: Dict[str, Any] | None = None,
            optimized: bool = False) -> BaseAlgorithm:

        if hyperparams is None:
            hyperparams = {
                "policy": "MlpPolicy",
            }

        kwargs = hyperparams.copy()

        if optimized:
            opt_hyperparams = hp.HYPERPARAMS_OPTIMIZED[self.algo]()
            kwargs.update(opt_hyperparams)

        model = ALGOS[self.algo](
            env=env,
            tensorboard_log=self.log_dir,
            verbose=self.verbose,
            device=self.device,
            **kwargs,
        )

        model.learn(total_timesteps=time_steps, tb_log_name=self.algo)
        return model

    @staticmethod
    def _evaluate(
            env: gym.Env,
            model: BaseAlgorithm,
            eval_episodes: int = 10,
            return_episode_rewards: bool = False):

        monitor_env = Monitor(env)
        rewards, steps = evaluate_policy(
            model,
            monitor_env,
            n_eval_episodes=eval_episodes,
            deterministic=True,
            return_episode_rewards=return_episode_rewards)

        return rewards, steps
