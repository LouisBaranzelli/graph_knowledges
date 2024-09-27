from typing import List, Optional
from dataStructure.BaseStructure import BaseStructure
from dataStructure.IQuerryManager import IQuerryManager
from dataStructure.Neo4jError import DataStructureArgumentException
from src.QuerryCypher.MainQuerry import DeleteQuerry, CreateQuerry, SetQuerry, MatchQuerry
from src.QuerryCypher.PatternQuerry import NodeNeo4j, Variable, PatternSet, PropertyNode, CypherDate


class RelationQuerryManager(BaseStructure, IQuerryManager):
    __name: str = 'Relation'

    def __init__(self, name: str, fromCategory: List[str], toCategory: List[str], message: Optional[str] = None,
                 hashValue: Optional[str] = None, dateCreation: Optional[str] = None):
        super().__init__(name, message, hashValue, dateCreation)
        self.__categories: List[str] = [RelationQuerryManager.__name]
        self.__fromCategory: str = ','.join([str(f) for f in fromCategory])
        self.__toCategory: str = ','.join([str(t) for t in toCategory])

    def getCategories(self) -> List[str]:
        return self.__categories

    def getDeleteQuerry(self) -> str:
        return str(DeleteQuerry([NodeNeo4j(category=self.__categories, variable='n', hashValue=self.getHashValue(),
                                           fromCategory=self.__fromCategory, toCategory=self.__toCategory)],
                                [Variable('n')]))

    def getCreateQuerry(self) -> str:

        node = NodeNeo4j(category=self.__categories, variable='n', name=self.getName(), message=self.getMessage(),
                         hash=self.getHashValue(), date_creation=CypherDate(self.getDateCreation().toString()))
        # setParameter wont block to overwrite an existing value of the Node on the DB even if different
        setParameter = [PatternSet(PropertyNode(node, 'name'), self.getName()),
                        PatternSet(PropertyNode(node, 'message'), self.getMessage()),
                        PatternSet(PropertyNode(node, 'date_creation'), self.getDateCreation().toString())
                        ]
        return str(CreateQuerry(value=NodeNeo4j(category=self.__categories, variable='n', hashValue=self.getHashValue(),
                                                fromCategory=self.__fromCategory, toCategory=self.__toCategory),
                                setValue=setParameter))

    def getModifyQuerry(self, propertyName: str, newValue: str | float) -> str:

        if propertyName in ["hashValue", "fromCategory", "toCategory"]:
            raise DataStructureArgumentException("Impossible to modify hashValue")

        if propertyName not in self.getPropertyNames():
            raise DataStructureArgumentException(f"Invalid property name: {propertyName}.")

        n = NodeNeo4j(variable='n', hashValue=self.getHashValue())
        return str(SetQuerry([n], PatternSet(PropertyNode(n, propertyName), newValue), outputs=[Variable('n')]))

    @staticmethod
    def getItemQuerry(name: str = None, hashValue: str = None, fromCategoryList: List[str] = None,
                      toCategoryList: List[str] = None) -> str:
        variable = Variable('n')
        category = [RelationQuerryManager.__name]
        fromCategory: str = ','.join([str(f) for f in fromCategoryList]) if fromCategoryList is not None else None
        toCategory: str = ','.join([str(t) for t in toCategoryList]) if toCategoryList is not None else None
        fromCategoryList, toCategoryList = None, None
        args = {k: v for k, v in locals().items() if v is not None}
        return str(MatchQuerry([NodeNeo4j(**args)], outputs=[Variable('n')]))

    @staticmethod
    def getStaticInstance() -> IQuerryManager:
        return RelationQuerryManager('', [], [], '', '')

    @staticmethod
    def getNameRelation() -> str:
        return RelationQuerryManager.__name
