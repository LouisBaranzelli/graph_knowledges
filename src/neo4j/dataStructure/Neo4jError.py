from src.common.ApplicationException import ApplicationException

from typing import List
from src.neo4j.dataStructure.BaseStructure import BaseStructure


class DataStructureException(ApplicationException):
    def __init__(self, message: str, level: int = 0):
        super().__init__(message, level)


class DataStructureExceptionException(DataStructureException):
    def __init__(self, elements: List[List[str]], message: str, level: int = 0):
        messages: list[str] = []
        [messages.append("[" + ' ,'.join([str(element_) for element_ in element]) + "]") for element in elements]
        message = f"{' AND '.join(messages)} not Compatible. {message}"
        super().__init__(message, level)


class DataStructureArgumentException(DataStructureException):
    def __init__(self, message: str, level: int = 0):
        super().__init__(message, level)


class DataBaseLogicException(DataStructureException):
    def __init__(self, message: str, level: int = 0):
        message = f"Request failed: {message}"
        super().__init__(message, level)
