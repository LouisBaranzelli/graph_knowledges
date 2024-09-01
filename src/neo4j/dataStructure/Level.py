import pytest
import math
from src.common.ConfigService import ConfigService as c
from src.common.TimeService import TimeNeo4j
from src.common.LogService import LogService, LogLevel


class Level:

    def __init__(self, level: int = 0, levelMax = c().getUserConfig().getLevelMax()):

        self.__level: int = level
        self.__levelMax = levelMax
        self.__levelMin = 0
        self.__level = min(max(level, self.__levelMin), self.__levelMax)

    def getLevel(self) -> int:
        return self.__level

    def upLevel(self) -> 'Level':
        return Level(min(self.__levelMax, self.__level + 1))

    def downLevel(self) -> 'Level':
        return Level(max(self.__levelMin, self.__level - 1))

    def getLevelMax(self) -> int:
        return self.__levelMax

    def getLevelMin(self) -> int:
        return self.__levelMin


class TimeCycle:

    def __init__(self, learningTime: int = c().getUserConfig().getLearningCycle(), learningCoef=c().getUserConfig().getLearningCoef()):

        self.__learningTime = learningTime
        self.__learningCoef = learningCoef

    def __getNextStepInDays(self, l: int, n: int) -> int:
        if l > n:
            LogService().write(f"Not step should be > than level, got: step: {n} and level: {l}. Return no change.", LogLevel.WARNING)
            return 0
        return math.ceil(self.__learningTime / (self.__learningCoef**(n-l)))

    def getNextStep(self, l: Level) -> TimeNeo4j:
        nbrDay = self.__getNextStepInDays(l=l.getLevel(), n=l.getLevelMax())
        return TimeNeo4j.getNow().addDay(nbrDay)
