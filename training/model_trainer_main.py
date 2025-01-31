import sys
from datetime import datetime, timezone, timedelta

import numpy as np
import torch as th

sys.path.append("../airflow/plugins")

from airflow.plugins.gym_env_factory import GymEnvFactory
from airflow.plugins.db_connection import DbConnection
from airflow.plugins.domain_model import Instrument, Interval
from airflow.plugins.gym_env_single_asset import register_single_asset_trading_env
from airflow.plugins.moex_candles_sql_adapter import CandlesSqlAdapter
from airflow.plugins.models_sql_adapter import ModelsSqlAdapter

from training.model_trainer import ModelTrainer

if __name__ == '__main__':
    algo = sys.argv[1]
    if algo is None:
        print(f"DRL algorithm as first argument must be specified.")
        print(f"Supported algorithms: a2c, ddpg, dqn, ppo, sac, td3, ars, qrdqn, tqc, trpo, ppo_lstm.")
        exit()

    print(f"Registering gym env...")
    register_single_asset_trading_env(1)

    db_connection = DbConnection.local_db_connection()
    instrument = Instrument.get_instrument("SBER")
    interval = Interval.min_10
    device = th.device("cuda" if th.cuda.is_available() else "cpu")

    sql_adapter = CandlesSqlAdapter(db_connection, interval, instrument)
    model_sql_adapter = ModelsSqlAdapter(db_connection)
    env_factory = GymEnvFactory(sql_adapter)

    trainer = ModelTrainer(
        env_factory=env_factory,
        algo=algo,
        verbose=0,
        device=device,
        seed=None,
        log_dir="logs",
    )

    train_end_time_utc = datetime(2025, 1, 30, tzinfo=timezone.utc)
    days_count = 100
    train_start_time_utc = train_end_time_utc - timedelta(days=days_count)

    basic_hyperparams = {
        "policy": "MlpPolicy",
    }

    print(f"Start training algorithm: {algo}")
    model = trainer.train(
        start_time_utc=train_start_time_utc,
        end_time_utc=train_end_time_utc,
        episode_duration=1000,
        episodes=100,
        hyperparams=basic_hyperparams,
        optimized=True)
    print("Training completed.")

    return_episode_rewards = False
    eval_episodes = 5

    eval_end_time_utc = datetime(2025, 1, 24, tzinfo=timezone.utc)
    eval_start_time_utc = eval_end_time_utc - timedelta(days=30)

    rewards, steps = trainer.evaluate(
        start_time_utc=eval_start_time_utc,
        end_time_utc=eval_end_time_utc,
        model=model,
        episode_duration=100,
        episodes=eval_episodes,
        return_episode_rewards=return_episode_rewards)

    if return_episode_rewards:
        print(f"{algo} evaluation: rewards={rewards} steps={steps}")
    else:
        print(f"{algo} reward evaluation by {eval_episodes} episodes: mean={rewards} std={steps}")

    model_name = f"{algo}_model"
    file_name = f"{model_name}.zip"

    # save into file
    print(f"Saving model to '{file_name}'")
    model.save(model_name)

    # save into db
    model_sql_adapter.insert_model(
        file_path=file_name,
        algo=algo,
        description=f"trained from {train_start_time_utc} to {train_end_time_utc}")

    version = model_sql_adapter.get_last_version(file_name)
    print(f"Model saved into db with version={version}")

