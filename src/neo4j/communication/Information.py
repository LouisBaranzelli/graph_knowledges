from abc import ABC
from typing import Optional, List, Tuple

from communication.CommonCommunication import IElement
from communication.Node import Node
from communication.Relation import Relation
from communication.ServerService import DriverNeo4j
from dataStructure.BaseStructure import BaseStructure
from dataStructure.InformationQuerryManager import InformationQuerryManager
from dataStructure.Level import Level
from dataStructure.Neo4jError import DataBaseLogicException
from dataStructure.NodeQuerryManager import NodeQuerryManager
from src.common.LogService import LogService
from src.common.TimeService import TimeNeo4j


class Information(IElement):

    def __init__(self, relation: Relation, fromNode: Node, toNode: Node,
                 level: Level = None, dateCreation: str = None, driver: DriverNeo4j = DriverNeo4j.getInstance()):
        IElement.__init__(self)

        self.__relation: Relation = relation
        self.__fromNode: Node = fromNode
        self.__toNode: Node = toNode
        self.__driver = driver
        if fromNode.isExist() is False or toNode.isExist() is False:
            raise DataBaseLogicException(f"Creation of the relation impossible. Node with hash: {fromNode.getHashValue()} or {toNode.getHashValue()} does not exist.")
        self.__querryManager = InformationQuerryManager(relation,
                                                        fromNode.getQuerryManager(),
                                                        toNode.getQuerryManager(),
                                                        level, dateCreation)

    def create(self, **kwargs) -> None:
        if self.isExist():
            raise DataBaseLogicException(f"Creation impossible. Relation: {self.__relation.getName()} between {self.__fromNode.getName()} and {self.__toNode.getName()} already existing.")

        if self.__relation.isExist() is False: # update the meta library of the existing relation
            self.__relation.create()

        self.__driver.send(querry=self.__querryManager.getCreateQuerry())

    def delete(self, **kwargs) -> None:
        pass

    def modify(self, **kwargs) -> None:
        pass

    def isExist(self) -> bool:
        res = len(Information.getItem(fromNodeHash=self.__fromNode.getHashValue(), toNodeHash=self.__toNode.getHashValue(), driver=self.__driver))
        if res == 1:
            return True
        elif res == 0:
            return False
        else:
            raise DataBaseLogicException(f"Node: {self.getName()} is existing several time.")

    @staticmethod
    def getItem(driver: DriverNeo4j = DriverNeo4j.getInstance(), fromNodeHash: str = None, fromCategory: List[str] = [],
                toNodeHash: str = None, toCategory: List[str] = [], relationHash: str = None) -> List:
        querryManagerStatic: InformationQuerryManager = InformationQuerryManager.getStaticInstance()
        output: List = driver.send(
            querryManagerStatic.getItemQuerry(fromNodeHash, fromCategory, toNodeHash, toCategory, relationHash))

        for o in output:
           a = Information.__deserializeRelation(o)

        return output

    @staticmethod
    def __deserialization(l: List) -> List['Information']:
        # output = [Node(category=list(r[0].labels), name=r[0].get('name'), message=r[0].get('message'),
        #                hashValue=r[0].get('hashValue'), date_creation=r[0].get('date_creation'),
        #                driver=DriverNeo4j.getInstance()) for r in l]
        # strResult = "\n".join([str(o) for o in output])


    @staticmethod
    def __deserializeNode(l: List) -> Tuple[Node, Node]:
        fromNode: Node = Node.deserialization([[l[0]]])[0]
        toNode: Node = Node.deserialization([[l[2]]])[0]
        return fromNode, toNode

    @staticmethod
    def __deserializeRelation(l: List) -> Relation:
        hashRelation: str = l[1]._properties['hashValue']
        if len(Relation.getItem(hashValue=hashRelation, driver=DriverNeo4j.getInstance())) != 1:
            assert DataBaseLogicException(f'The relation with the hash {hashRelation} is used but the meta relation does not exist.')
        return Relation.getItem(hashValue=hashRelation, driver=DriverNeo4j.getInstance())[0]

        # LogService().debug(f"Deserialisation: got: {l}\nSent: {strResult}")
        # return output
        return []
