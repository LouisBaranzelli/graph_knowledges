from typing import List, Optional

from dataStructure.IQuerryManager import IQuerryManager
from src.QuerryCypher.MainQuerry import CreateQuerry, NodeNeo4j, SetQuerry, DeleteQuerry, MatchQuerry
from src.QuerryCypher.PatternQuerry import PatternSet, PropertyNode, CypherDate, Variable, PatternQuerry
from src.common.TimeService import TimeNeo4j
from src.neo4j.dataStructure.BaseStructure import BaseStructure
from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException


class NodeQuerryManager(BaseStructure, IQuerryManager):

    def __init__(self, name: str, category: str | List[str], message: Optional[str] = None, hashValue: Optional[str] = None, dateCreation: Optional[str] = None):
        super().__init__(name, message, hashValue, dateCreation)
        self.__categories: List[str] = [category.capitalize()] if isinstance(category, str) else [element.capitalize() for element in category]

    def getCategories(self) -> List[str]:
        return self.__categories

    def getDeleteQuerry(self) -> str:
        return str(DeleteQuerry([NodeNeo4j(category=self.__categories, variable='n', hashValue=self.getHashValue())], [Variable('n')]))

    def getCreateQuerry(self) -> str:

        node = NodeNeo4j(category=self.__categories, variable='n', name=self.getName(), message=self.getMessage(), hash=self.getHashValue(), date_creation=CypherDate(self.getTimeCreation().toString()))
        setParameter = [PatternSet(PropertyNode(node, 'name'), self.getName()),
                        PatternSet(PropertyNode(node, 'message'), self.getMessage()),
                        PatternSet(PropertyNode(node, 'date_creation'), self.getTimeCreation().toString())
                        ]
        return str(CreateQuerry(value=NodeNeo4j(category=self.__categories, variable='n', hashValue=self.getHashValue()), setValue=setParameter))

    def getModifyQuerry(self, propertyName: str, newValue: str | float) -> str:

        if propertyName == "hashValue":
            raise DataStructureArgumentException("Impossible to modify hashValue")

        if propertyName not in self.getPropertyNames():
            raise DataStructureArgumentException(f"Invalid property name: {propertyName}.")

        n = NodeNeo4j(variable='n', hashValue=self.getHashValue())
        return str(SetQuerry([n], PatternSet(PropertyNode(n, propertyName), newValue), outputs=[Variable('n')]))

    @staticmethod
    def getItemQuerry(category: List[str] = [], name: str=None, hashValue: str = None) -> str:
        variable = Variable('n')
        args = {k: v for k, v in locals().items() if v is not None}
        return str(MatchQuerry([NodeNeo4j(**args)], outputs=[Variable('n')]))

    @staticmethod
    def getStaticInstance() -> IQuerryManager:
        return NodeQuerryManager('', '', '', '')

