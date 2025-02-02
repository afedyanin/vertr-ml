from enum import Enum


class StrategyType(str, Enum):
    Sb3 = 'Sb3'
    RandomWalk = 'RandomWalk'
    TrendFollowing = 'TrendFollowing'


class Action(int, Enum):
    Hold = 0
    Sell = 1
    Buy = 2
