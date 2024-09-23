from abc import ABC
from typing import Optional, List
from dataStructure.BaseStructure import BaseStructure
from src.common.TimeService import TimeNeo4j


class Relation(BaseStructure, ABC):

    def __init__(self, fromCategory: List[str], toCategory: List[str], name: str, message: Optional[str] = None,
                 hashValue: Optional[str] = None, date_creation: TimeNeo4j = None):
        BaseStructure.__init__(self, name, message, hashValue, date_creation)
        self.__category: List[str] = ['INFORMATION']
        self.__fromCategory: List[str] = [f.capitalize() for f in fromCategory]
        self.__toCategory: List[str] = [t.capitalize() for t in toCategory]

    def getFromCategory(self) -> List[str]:
        return self.__fromCategory

    def getToCategory(self) -> List[str]:
        return self.__toCategory
