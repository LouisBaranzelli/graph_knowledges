from typing import List, Optional

from communication.Relation import Relation
from dataStructure.IQuerryManager import IQuerryManager
from dataStructure.Level import Level, TimeCycle
from dataStructure.NodeQuerryManager import NodeQuerryManager
from src.common.TimeService import TimeNeo4j
from src.neo4j.dataStructure.BaseStructure import BaseStructure
from src.QuerryCypher.MainQuerry import MatchQuerry, SetQuerry, CreateQuerry, DeleteQuerry
from src.QuerryCypher.PatternQuerry import PatternQuerry, NodeNeo4j, RelationNeo4j, Variable, PatternSet, PropertyNode, \
    CypherDate
from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException


class InformationQuerryManager(IQuerryManager):
    __category: str = 'INFORMATION'

    def __init__(self, relation: Relation, fromNode: NodeQuerryManager = None, toNode: NodeQuerryManager = None,
                 level: Level = None, dateCreation: str = None):

        self.__level = Level() if level is None else level
        self.__dateCreation: TimeNeo4j = TimeNeo4j.getNow() if dateCreation is None else TimeNeo4j.fromString(
            dateCreation)
        self.__relation: Relation = relation
        self.__propertyNames = ['level', 'dateCreation']
        self.__fromNode: NodeQuerryManager = fromNode
        self.__toNode: NodeQuerryManager = toNode
        # pas de hash Value pour l'information (seulement pour la Relation general),
        # car information peut etre identifiee par les hashs des noeuds

    def getModifyQuerry(self, propertyName: str, newValue: str | float) -> str:

        if propertyName == "hashValue":
            raise DataStructureArgumentException("Impossible to modify hashValue")

        if propertyName not in self.__propertyNames:
            raise DataStructureArgumentException(f"Invalid property name: {propertyName}.")

        fromNode: NodeNeo4j = NodeNeo4j(hashValue=self.__fromNode.getHashValue())
        toNode: NodeNeo4j = NodeNeo4j(hashValue=self.__toNode.getHashValue())

        r: RelationNeo4j = RelationNeo4j(category=InformationQuerryManager.__category, variable='r')
        p: PatternQuerry = PatternQuerry(fromNode, r, toNode)
        return str(SetQuerry([p], PatternSet(PropertyNode(r, propertyName), newValue)))

    @staticmethod
    def getItemQuerry(fromNodeHash: str = None, fromCategory: List[str] = [], toNodeHash: str = None, toCategory: List[str] = [], **kwargs) -> str:

        propLeft = {'hashValue': fromNodeHash, 'category': fromCategory}
        propLeft = {key: value for key, value in propLeft.items() if value not in [None, []]}
        fromNode: NodeNeo4j = NodeNeo4j(variable='n1', **propLeft)

        propRight = {'hashValue': toNodeHash, 'category': toCategory}
        propRight = {key: value for key, value in propRight.items() if value not in [None, []]}
        toNode: NodeNeo4j = NodeNeo4j(variable='n2', **propRight)

        r: RelationNeo4j = RelationNeo4j(category=InformationQuerryManager.__category, variable='r')

        p = PatternQuerry(fromNode, r , toNode)
        return str(MatchQuerry(inputs=[p], outputs=[Variable('r')]))

    def getCreateQuerry(self) -> str:

        if not all([f in self.__fromNode.getCategories() for f in self.__relation.getFromCategory()]):
            raise DataStructureArgumentException(
                f"Left node {self.__fromNode.getCategories()} doesn't match with the expected category of the relation: {self.__relation.getFromCategory()}.")
        if not all([t in self.__toNode.getCategories() for t in self.__relation.getToCategory()]):
            raise DataStructureArgumentException(
                f"Right node {self.__toNode.getCategories()} doesn't match with the expected category of the relation: {self.__relation.getToCategory()}.")

        r = RelationNeo4j(category=InformationQuerryManager.__category, variable='r',
                          hashValue=self.__relation.getHashValue(), date_creation=self.getDateCreation().toString(),
                          level=self.__level.getLevel(), updateTime=TimeCycle().getNextStep(self.__level).toString(),
                          toRight=True)

        fromNodeNeo4j: NodeNeo4j = NodeNeo4j(variable='n1', hashValue=self.__fromNode.getHashValue())
        toNodeNeo4j: NodeNeo4j = NodeNeo4j(variable='n2', hashValue=self.__toNode.getHashValue())

        matchQuerry: str = str(MatchQuerry(inputs=[fromNodeNeo4j, toNodeNeo4j]))
        createQuerry: str = str(CreateQuerry(PatternQuerry(NodeNeo4j(variable='n1'), r, NodeNeo4j(variable='n2'))))
        return matchQuerry + createQuerry

    def getDeleteQuerry(self) -> str:

        fromNodeNeo4j: NodeNeo4j = NodeNeo4j(variable='n1', hashValue=self.__fromNode.getHashValue())
        toNodeNeo4j: NodeNeo4j = NodeNeo4j(variable='n2', hashValue=self.__toNode.getHashValue())
        return str(DeleteQuerry([PatternQuerry(fromNodeNeo4j,
                                               RelationNeo4j(category=InformationQuerryManager.__category,
                                                             variable='r'), toNodeNeo4j)], [Variable('r')]))

    @staticmethod
    def getStaticInstance() -> 'IQuerryManager':
        pass

    def getLevel(self) -> Level:
        return self.__level

    def getRelation(self) -> Relation:
        return self.__relation

    def getDateCreation(self) -> TimeNeo4j:
        return self.__dateCreation
