from typing import List, Optional

from src.neo4j.dataStructure.BaseStructure import BaseStructure
from src.QuerryCypher.MainQuerry import MatchQuerry, SetQuerry
from src.QuerryCypher.PatternQuerry import PatternQuerry, NodeNeo4j, RelationNeo4j, Variable, PatternSet, PropertyNode
from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException


class RelationApplication(BaseStructure, IBaseStructure):

    __toCategories: List[str]
    __fromCategories: List[str]


    def __init__(self, name: str, fromCategory: str | List[str], toCategory: Optional[str | List[str]] = None, message: Optional[str] = None, hash: Optional[str] = None):
        super().__init__(name, message, hash)
        self.__fromCategories: List[str] = [fromCategory.capitalize()] if isinstance(fromCategory, str) else [element.capitalize() for element in fromCategory]
        self.__toCategories: List[str] = [] if toCategory is None else [toCategory] if isinstance(toCategory, str) else [element.capitalize() for element in toCategory]
        self.__occurrence: int = 0

        self.getPropertyNames().append(['occurrence', 'update'])

    def getFromCategories(self) -> List[str]:
        return self.__fromCategories

    def getOccurrence(self) -> int:
        return self.__occurrence

    def getToCategories(self) -> List[str]:
        return self.__toCategories

    def getModifyQuerry(self, propertyName: str, newValue: str | float) -> str:

        if propertyName == "hashValue":
            raise DataStructureArgumentException("Impossible to modify hashValue")

        if propertyName not in self.getPropertyNames():
            raise DataStructureArgumentException(f"Invalid property name: {propertyName}.")

        r = RelationNeo4j(variable='r', hash=self.getHashValue())
        return str(SetQuerry([PatternQuerry(NodeNeo4j(), r, NodeNeo4j())], PatternSet(PropertyNode(r, propertyName), newValue)))

    @staticmethod
    def getAllQuerry(categoryRel: List[str] = [], fromCategory: List[str] = [], toCategory: List[str] = []) -> str:

        r = RelationNeo4j(category=categoryRel, variable='r') if len(fromCategory + toCategory) == 0 else RelationNeo4j(category=categoryRel, variable='r', toRight=True)
        p = PatternQuerry(NodeNeo4j(category=fromCategory), r, NodeNeo4j(category=toCategory))
        return str(MatchQuerry(inputs=[p], outputs=[Variable('r')]))



if __name__ == '__main__':
    Relation('louis', ['Personne', 'annimal'], ['Personne', 'annimal'])

