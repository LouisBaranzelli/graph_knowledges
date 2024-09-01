from typing import List, Optional
from src.QuerryCypher.MainQuerry import CreateQuerry, NodeNeo4j, SetQuerry, DeleteQuerry, MatchQuerry
from src.QuerryCypher.PatternQuerry import PatternSet, PropertyNode, CypherDate, Variable, PatternQuerry
from src.common.TimeService import TimeNeo4j
from src.neo4j.dataStructure.BaseStructure import BaseStructure
from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException


class NodeApplication(BaseStructure, IBaseStructure):

    def __init__(self, name: str, category: str | List[str], message: Optional[str] = None, hashValue: Optional[str] = None):
        super().__init__(name, message, hashValue)
        self.__categories: List[str] = [category.capitalize()] if isinstance(category, str) else [element.capitalize() for element in category]

    def getCategories(self) -> List[str]:
        return self.__categories

    def getDeleteQuerry(self) -> str:
        return str(DeleteQuerry([NodeNeo4j(category=self.__categories, variable='n', hash=self.getHashValue())], [Variable('n')]))

    def getCreateQuerry(self) -> str:
        return str(CreateQuerry(NodeNeo4j(category=self.__categories, variable='n', name=self.getName(), message=self.getMessage(), hash=self.getHashValue(), date_creation=CypherDate(self.getTimeCreation().toString()), occurrence=0)))

    def getModifyQuerry(self, propertyName: str, newValue: str | float) -> str:

        if propertyName == "hashValue":
            raise DataStructureArgumentException("Impossible to modify hashValue")

        if propertyName not in self.getPropertyNames():
            raise DataStructureArgumentException(f"Invalid property name: {propertyName}.")

        n = NodeNeo4j(variable='n', hash=self.getHashValue())
        return str(SetQuerry([n], PatternSet(PropertyNode(n, propertyName), newValue)))

    @staticmethod
    def getItemQuerry(category: List[str] = [], name: str=None, hashValue: str = None) -> str:
        variable = Variable('n')
        args = {k: v for k, v in locals().items() if v is not None}
        return str(MatchQuerry([NodeNeo4j(**args)], outputs=[Variable('n')]))


if __name__ == '__main__':
    a = Node(name='louis', category='Personne')
    print(a.getModifyQuerry(propertyName='name', newValue='pierre'))

