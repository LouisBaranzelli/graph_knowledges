from typing import List, Optional

from dataStructure.IQuerryManager import IQuerryManager
from dataStructure.Level import Level, TimeCycle
from dataStructure.NodeQuerryManager import NodeQuerryManager
from src.common.TimeService import TimeNeo4j
from src.neo4j.dataStructure.BaseStructure import BaseStructure
from src.QuerryCypher.MainQuerry import MatchQuerry, SetQuerry, CreateQuerry, DeleteQuerry
from src.QuerryCypher.PatternQuerry import PatternQuerry, NodeNeo4j, RelationNeo4j, Variable, PatternSet, PropertyNode, \
    CypherDate
from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException


class RelationQuerryManager(BaseStructure, IQuerryManager):

    __category: str = 'INFORMATION'

    def __init__(self, name: str, fromCategory: List[str], toCategory: List[str], message: Optional[str] = None, hashValue: Optional[str] = None, level: int = 0, update: TimeNeo4j = None):
        '''fromCategory and toCategory required to protect the relation creation from wrong elements node'''
        super().__init__(name, message, hashValue)
        self.__fromCategories: List[str] = [fromCategory.capitalize()] if isinstance(fromCategory, str) else [element.capitalize() for element in fromCategory]
        self.__toCategories: List[str] = [] if toCategory is None else [toCategory] if isinstance(toCategory, str) else [element.capitalize() for element in toCategory]
        self.__level: Level = Level(level)
        self.__update: TimeNeo4j = TimeCycle().getNextStep(self.__level) if update is None else update
        [self.getPropertyNames().append(e) for e in ['update', 'level']]

    def getFromCategories(self) -> List[str]:
        return self.__fromCategories

    def getToCategories(self) -> List[str]:
        return self.__toCategories

    def getModifyQuerry(self, propertyName: str, newValue: str | float) -> str:
        #TODO Verifier si les relation d'un meme Hash partagent toutes les memes caracteristiques, dans le cas contraire, identifier les relation par les noeuds from et to
        if propertyName == "hashValue":
            raise DataStructureArgumentException("Impossible to modify hashValue")

        if propertyName not in self.getPropertyNames():
            raise DataStructureArgumentException(f"Invalid property name: {propertyName}.")

        r = RelationNeo4j(category=RelationQuerryManager.__category, variable='r', hash=self.getHashValue())
        return str(SetQuerry([PatternQuerry(NodeNeo4j(), r, NodeNeo4j())], PatternSet(PropertyNode(r, propertyName), newValue)))

    @staticmethod
    def getItemQuerry(fromNodeHash: str = None, fromCategory: List[str] = [], toNodeHash: str = None, toCategory: List[str] = [], **kwargs) -> str:

        propLeft = {'hashValue': fromNodeHash, 'category': fromCategory}
        propLeft = {key: value for key, value in propLeft.items() if value not in [None, []]}
        fromNode: NodeNeo4j = NodeNeo4j(variable='n1', **propLeft)

        propRight = {'hashValue': toNodeHash, 'category': toCategory}
        propRight = {key: value for key, value in propRight.items() if value not in [None, []]}
        toNode: NodeNeo4j = NodeNeo4j(variable='n2', **propRight)

        p = PatternQuerry(fromNode, RelationNeo4j(category=RelationQuerryManager.__category, variable='r', **kwargs), toNode)
        return str(MatchQuerry(inputs=[p], outputs=[Variable('r')]))

    def getCreateQuerry(self, fromNode: NodeQuerryManager = None, toNode: NodeQuerryManager = None) -> str:
        ''' Les noeud doivent avoir ete cree en amont '''

        if not all([f in fromNode.getCategories() for f in self.__fromCategories]):
            raise DataStructureArgumentException(f"Left node {fromNode.getCategories()} doesn't match with the expected category of the relation: {self.__fromCategories}.")
        if not all([t in toNode.getCategories() for t in self.__toCategories]):
            raise DataStructureArgumentException(f"Right node {toNode.getCategories()} doesn't match with the expected category of the relation: {self.__toCategories}.")

        r = RelationNeo4j(category=RelationQuerryManager.__category, variable='r', name=self.getName(), message=self.getMessage(),
                          hashValue=self.getHashValue(), date_creation=CypherDate(TimeNeo4j.getNow().toString()),
                          level=self.__level.getLevel(), update=self.__update.toString(), toRight=True)

        fromNodeNeo4j: NodeNeo4j = NodeNeo4j(variable='n1', hashValue=fromNode.getHashValue())
        toNodeNeo4j: NodeNeo4j = NodeNeo4j(variable='n2', hashValue=toNode.getHashValue())

        matchQuerry: str = str(MatchQuerry(inputs=[fromNodeNeo4j, toNodeNeo4j]))
        createQuerry:str = str(CreateQuerry(PatternQuerry(NodeNeo4j(variable='n1'), r, NodeNeo4j(variable='n2'))))
        return matchQuerry + createQuerry

    def getDeleteQuerry(self, fromNode: NodeQuerryManager = None, toNode: NodeQuerryManager = None) -> str:
        fromNodeNeo4j: NodeNeo4j = NodeNeo4j(variable='n1', hashValue=fromNode.getHashValue())
        toNodeNeo4j: NodeNeo4j = NodeNeo4j(variable='n2', hashValue=toNode.getHashValue())

        return str(DeleteQuerry([PatternQuerry(fromNodeNeo4j, RelationNeo4j(category=RelationQuerryManager.__category, variable='r', hashValue=self.getHashValue()), toNodeNeo4j)], [Variable('r')]))
        # ecrire le teste + ajouter un teste a la creation de la relation queles typoe concorde si non exception

    @staticmethod
    def getStaticInstance() -> 'IQuerryManager':
        pass