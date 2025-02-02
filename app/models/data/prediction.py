from enum import Enum


class StrategyType(str, Enum):
    Sb3 = 'Sb3'
    RandomWalk = 'RandomWalk'
    TrendFollowing = 'TrendFollowing'
