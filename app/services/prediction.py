import abc
from datetime import datetime, timezone
from enum import Enum
from random import Random
from typing import List

from app.configuration.config import PgSqlSettings
from app.models.gym_env_single_asset import Action
from app.models.request.prediction import PredictionRequest, PredictionResult, PredictionItem
from app.repositories.tinvest_candles import TinvestCandlesRepository


