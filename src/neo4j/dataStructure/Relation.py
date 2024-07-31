from typing import List, Optional
from src.neo4j.dataStructure.BaseStructure import BaseStructure


class Relation(BaseStructure):

    __toCategories: list[str]
    __fromCategories: list[str]

    def __init__(self, name: str, fromCategory: str | List[str], toCategory: Optional[str | List[str]] = None, message: Optional[str] = None, hash: Optional[str] = None):
        super().__init__(name, message, hash)
        self.__fromCategories: List[str] = [fromCategory.capitalize()] if isinstance(fromCategory, str) else [element.capitalize() for element in fromCategory]
        self.__toCategories: List[str] = [] if toCategory is None else [toCategory] if isinstance(toCategory, str) else [element.capitalize() for element in toCategory]

    def getFromCategories(self) -> List[str]:
        return self.__fromCategories

    def getToCategories(self) -> List[str]:
        return self.__toCategories


if __name__ == '__main__':
    Relation('louis', ['Personne', 'annimal'], ['Personne', 'annimal'])

