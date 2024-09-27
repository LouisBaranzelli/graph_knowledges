from typing import Optional, List

from communication.ServerService import DriverNeo4j
from dataStructure.RelationQuerryManager import RelationQuerryManager
from src.common.LogService import LogService
from src.common.TimeService import TimeNeo4j
from communication.Node import Node


class Relation(Node):

    def __init__(self, fromCategory: List[str], toCategory: List[str], name: str, message: Optional[str] = None,
                 hashValue: Optional[str] = None, dateCreation: TimeNeo4j = None, driver: DriverNeo4j = DriverNeo4j.getInstance()):

        Node.__init__(self, name, RelationQuerryManager.getNameRelation(), message, hashValue, dateCreation, driver)

        self.__category: List[str] = ['INFORMATION'] # Nom de la category de toutes les Informations (pas relation) entre les noeuds
        self.__fromCategory: List[str] = [f.capitalize() for f in fromCategory]
        self.__toCategory: List[str] = [t.capitalize() for t in toCategory]
        self.setQuerryManager(RelationQuerryManager(name, fromCategory, toCategory, message, hashValue, dateCreation))

    def getFromCategory(self) -> List[str]:
        return self.__fromCategory

    def getToCategory(self) -> List[str]:
        return self.__toCategory

    @staticmethod
    def deserialization(l: List) -> List['Relation']:
        output = [Relation(fromCategory=r[0].get('fromCategory').split(','), toCategory=r[0].get('toCategory').split(','),  name=r[0].get('name'), message=r[0].get('message'),
                       hashValue=r[0].get('hashValue'), dateCreation=r[0].get('date_creation'),
                       driver=DriverNeo4j.getInstance()) for r in l]
        strResult = "\n".join([str(o) for o in output])
        LogService().debug(f"Deserialisation: got: {l}\nSent: {strResult}")
        return output

    @staticmethod
    def getItem(fromCategory: List[str] = None, toCategory: List[str] = None , name: str = None, hashValue: str = None,
                driver: DriverNeo4j = DriverNeo4j().getInstance()) -> List['Node']:
        querryManagerStatic: RelationQuerryManager = RelationQuerryManager.getStaticInstance()
        results: List = driver.send(querry=querryManagerStatic.getItemQuerry(name, hashValue, fromCategory, toCategory))
        return Relation.deserialization(results)

    def getFromCategory(self) -> List[str]:
        return self.__fromCategory

    def getToCategory(self) -> List[str]:
        return self.__toCategory
