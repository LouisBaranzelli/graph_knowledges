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


class RelationQuerryManager(BaseStructure, IQuerryManager):

    __category: str = 'INFORMATION'

    def __init__(self, relation: Relation, fromNode: NodeQuerryManager = None, toNode: NodeQuerryManager = None, level: Level = None, dateCreation: str = None):
        # ajouter IQuerryManager
        self.__level = Level() if level is None else level
        self.__dateCreation: TimeNeo4j = TimeNeo4j.getNow() if dateCreation is None else TimeNeo4j.fromString(dateCreation)
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

    def getDateCreation(self) -> TimeNeo4j:
        return self.__dateCreation