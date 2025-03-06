import sys
from datetime import datetime, timezone, timedelta

import torch as th

from app.configuration.config import PgSqlSettings
from app.models.data.candle import Interval
from app.models.gym_env_factory import register_single_asset_trading_env
from app.repositories.sb3_models import Sb3ModelsRepository
from app.repositories.tinvest_candles import TinvestCandlesRepository
from training.model_trainer import ModelTrainer

if __name__ == '__main__':
    algo = sys.argv[1]
    if algo is None:
        print(f"DRL algorithm as first argument must be specified.")
        print(f"Supported algorithms: a2c, ddpg, dqn, ppo, sac, td3, ars, qrdqn, tqc, trpo, ppo_lstm.")
        exit()

    print(f"Registering gym env...")
    register_single_asset_trading_env(1)

    sql_config = PgSqlSettings(_env_file='../app/.env')
    candles_repo = TinvestCandlesRepository(sql_config)
    models_repo = Sb3ModelsRepository(sql_config)

    symbol = "SBER"
    interval = Interval.CANDLE_INTERVAL_10_MIN
    device = th.device("cuda" if th.cuda.is_available() else "cpu")

    train_end_time_utc = datetime(2025, 3, 5, tzinfo=timezone.utc)
    train_start_time_utc = train_end_time_utc - timedelta(days=100)
    eval_end_time_utc = datetime(2025, 3, 5, tzinfo=timezone.utc)
    eval_start_time_utc = eval_end_time_utc - timedelta(days=30)

    train_candles = candles_repo.get_candles(
        symbol=symbol,
        interval=interval.value,
        start_date_utc=train_start_time_utc,
        end_date_utc=train_end_time_utc)

    trainer = ModelTrainer(
        algo=algo,
        verbose=0,
        device=device,
        log_dir="logs",
    )

    basic_hyperparams = {
        "policy": "MlpPolicy",
    }

    print(f"Start training algorithm: {algo}")
    model = trainer.train(
        candles_df=train_candles,
        episode_duration=1000,
        episodes=100,
        hyperparams=basic_hyperparams,
        optimized=True)
    print("Training completed.")

    return_episode_rewards = False
    eval_episodes = 5

    eval_candles = candles_repo.get_candles(
        symbol=symbol,
        interval=interval.value,
        start_date_utc=eval_start_time_utc,
        end_date_utc=eval_end_time_utc)

    rewards, steps = trainer.evaluate(
        candles_df=eval_candles,
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
    models_repo.insert_model(
        file_path=file_name,
        algo=algo,
        description=f"{symbol} on {interval.name}. From {train_start_time_utc} to {train_end_time_utc}")

    version = models_repo.get_last_version(file_name)
    print(f"Model saved into db with version={version}")

