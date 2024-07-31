from typing import List, Optional
from src.neo4j.dataStructure.BaseStructure import BaseStructure


class Node(BaseStructure):

    __categories: list[str]

    def __init__(self, name: str, category: str | List[str], message: Optional[str] = None, hash: Optional[str] = None):
        super().__init__(name, message, hash)
        self.__categories: List[str] = [category.capitalize()] if isinstance(category, str) else [element.capitalize() for element in category]

    def getCategories(self) -> List[str]:
        return self.__categories


if __name__ == '__main__':
    Node('louis', ['Personne', 'annimal'])

