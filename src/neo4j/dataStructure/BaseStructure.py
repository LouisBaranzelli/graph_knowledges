import datetime
import uuid
from typing import Optional, List
from src.common.TimeService import TimeNeo4j


class BaseStructure:

    __hashValue: str
    __name: str
    __message: str | None
    __propertyName: list[str]

    def __init__(self, name: str, message: Optional[str] = None, hashValue: [str] = None, dateCreation: str = None):

        self.__hashValue: str = str(uuid.uuid4() if hashValue is None else hashValue)
        self.__name: str = name
        self.__message: str = message or ''
        self.__dateCreation: TimeNeo4j = TimeNeo4j.getNow() if dateCreation is None else TimeNeo4j.fromString(dateCreation)
        self.__propertyNames = ['hashValue', 'message', 'dateCreation', 'name']

    def getHashValue(self) -> str:
        return self.__hashValue

    def getDateCreation(self) -> TimeNeo4j:
        return self.__dateCreation

    def getName(self) -> str:
        return self.__name

    def getMessage(self) -> str:
        return self.__message

    def getPropertyNames(self) -> List[str]:
        return self.__propertyNames


