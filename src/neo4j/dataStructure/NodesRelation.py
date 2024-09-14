from datetime import datetime
from src.neo4j.dataStructure.BaseStructure import BaseStructure
from src.neo4j.dataStructure.Relation import Relation
from communication.Node import Node
from src.neo4j.dataStructure.Neo4jError import DataStructureExceptionException


class NodesRelation(BaseStructure):

    __compteur: int
    __dateCreation: datetime

    def __init__(self, nodeLeft: Node, relation: Relation, nodeRight: Node, dateCreation: [datetime] = None, compteur: [int] = None):
        if not all([catRelLeft in nodeLeft.getCategories() for catRelLeft in relation.getFromCategories()]):
            raise DataStructureExceptionException([nodeLeft.getCategories(), relation.getFromCategories()],
                                         "Categories don't match in left hand.")
        if not all([catRelRight in nodeRight.getCategories() for catRelRight in relation.getToCategories()]):
            raise DataStructureExceptionException([nodeRight.getCategories(), relation.getToCategories()],
                                         "Categories don't match in right hand.")

        self.__dateCreation: datetime = datetime.now() if dateCreation is None else dateCreation
        self.__compteur: int = 0 if dateCreation is None else compteur

    def getDateCreation(self) -> datetime:
        return self.__dateCreation

    def getCompteur(self) -> int:
        return self.__compteur




