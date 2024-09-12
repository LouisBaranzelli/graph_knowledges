from typing import Optional, List

from communication.CommonCommunication import IElement
from communication.ServerService import DriverNeo4j
from dataStructure.BaseStructure import BaseStructure
from dataStructure.Neo4jError import DataBaseLogicException
from dataStructure.NodeQuerryManager import NodeQuerryManager
from src.common.TimeService import TimeNeo4j


class Node(IElement, BaseStructure):

    def __init__(self, name: str, category: str | List[str], message: Optional[str] = None,
                 hashValue: Optional[str] = None, date_creation: TimeNeo4j = None,
                 driver: DriverNeo4j = DriverNeo4j.getInstance()):
        IElement.__init__(self)
        BaseStructure.__init__(self, name, message, hashValue, date_creation)
        self.__category: List[str] = [category.capitalize()] if isinstance(category, str) else [element.capitalize()
                                                                                                for element in
                                                                                                category]
        self.__driver = driver
        self.__querryManager = NodeQuerryManager(name, category, message, hashValue, date_creation)

    def create(self, **kwargs) -> None:
        if self.isExist():
            raise DataBaseLogicException(f"Creation impossible. Node: {self.getName()} already existing.")
        self.__driver.send(querry=self.__querryManager.getCreateQuerry())

    def delete(self, **kwargs) -> None:
        if self.isExist() is False:
            raise DataBaseLogicException(f"Deletion impossible. Node: {self.getName()} does not exist.")
        self.__driver.send(querry=self.__querryManager.getDeleteQuerry())

    def modify(self, propertyName: str, newValue: str | float) -> 'Node':
        if self.isExist() is False:
            raise DataBaseLogicException(f"Modification impossible. Node: {self.getName()} not existing anymore.")
        r: List = self.__driver.send(querry=self.__querryManager.getModifyQuerry(propertyName, newValue))
        return Node(category=list(r[0][0].labels), name=r[0][0].get('name'), message=r[0][0].get('message'),
                    hashValue=r[0][0].get('hashValue'), date_creation=r[0][0].get('date_creation'), driver=DriverNeo4j.getInstance())

    def getCategory(self) -> List[str]:
        return self.__category

    def isExist(self) -> bool:
        return len(Node.getItem(hashValue=self.getHashValue(), driver=self.__driver)) == 1

    @staticmethod
    def getItem(category: List[str] = [], name: str = None, hashValue: str = None,
                driver: DriverNeo4j = DriverNeo4j().getInstance()) -> List['Node']:
        querryManagerStatic: NodeQuerryManager = NodeQuerryManager.getStaticInstance()
        results: List = driver.send(querry=querryManagerStatic.getItemQuerry(category, name, hashValue))
        return [Node(category=list(r[0].labels), name=r[0].get('name'), message=r[0].get('message'),
                     hashValue=r[0].get('hashValue'), date_creation=r[0].get('date_creation'), driver=DriverNeo4j.getInstance()) for r in results]