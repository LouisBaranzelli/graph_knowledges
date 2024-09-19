import json
from typing import Dict, Type, Set

from src.utils.Constant import CONFIG_PATH
from src.common.LogService import LogService, LogLevel


class Parameter():

    def __init__(self, value, min: object = None, max: object = None, classAutorized: Type = object):

        self.__value: object = None
        self.__classAutorized = classAutorized
        self.__min: float | int = min
        self.__max: float | int = max
        self.set(value)

    def set(self, v: object) -> bool:

        if not isinstance(v, self.__classAutorized):
            LogService().debug(f'Wrong instance. Expected{self.__classAutorized}, got {type(v)}')
            return False

        if isinstance(v, (int, float)):
            if self.__max is not None:
                if v > self.__max:
                    LogService().debug(f'Wrong value. Max: {self.__max}, got {v}')
                    self.__value = self.__max
                    return False
                if v < self.__min:
                    LogService().debug(f'Wrong value. Min: {self.__min}, got {v}')
                    self.__value = self.__min
                    return False

        self.__value = v
        return True

    def get(self) -> object:
        return self.__value


class BaseConfig:

    def __init__(self, **kwargs):
        [LogService().debug(f"Argument non autorisé : {key}", LogLevel.WARNING) for key in kwargs]

        # if not all([requiredKey in kwargs for requiredKey in allowed_args]):
        #     raise ApplicationException(f'Missing argument in config file: {[requiredKey for requiredKey in allowed_args  if requiredKey not in kwargs]}')


class UserConfig(BaseConfig):

    def __init__(self, learningCycle: int = 180, levelMax: int = 10, learningCoef=1.7, **kwargs):
        super().__init__(**kwargs)

        self.__levelMax: Parameter = Parameter(levelMax, classAutorized=int, min=1, max=20)
        self.__learningCoef: Parameter = Parameter(learningCoef, classAutorized=float, min=1.5, max=2.5)
        minLearningCycle = (learningCoef + 1) ** self.__levelMax.get()
        self.__learningCycle: Parameter = Parameter(learningCycle, classAutorized=int, min=minLearningCycle)

    def getLevelMax(self) -> int:
        return self.__levelMax.get()

    def getLearningCycle(self) -> int:
        return self.__learningCycle.get()

    def getLearningCoef(self) -> float:
        return self.__learningCoef.get()


class ConfigService:
    __instance: 'ConfigService' = None
    __flagInitialized: bool = False

    def __init__(self, pathConfig: str = CONFIG_PATH):

        if not ConfigService.__flagInitialized:
            with open(pathConfig, 'r') as f:
                config_data = json.load(f)

            self.__userConfig = UserConfig(**config_data['user'])

            ConfigService.__flagInitialized = True

    def getUserConfig(self) -> UserConfig:
        return self.__userConfig

    def reset(self):
        ConfigService.__instance = None
        ConfigService.__flagInitialized = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance
