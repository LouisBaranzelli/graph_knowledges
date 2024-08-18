from typing import List, Optional, Union
from CypherException import QuerryException
from utils import StringFunctions, FiguresFunctions, ListUtils


class Property:
    __value: str | float
    __name: str

    def __init__(self, name: str | int, value: str | int | float):
        self.__name: str = str(name)
        self.__value: str | float = value if isinstance(value, str) else FiguresFunctions.convertInFloat(value)

    def getName(self) -> str:
        return self.__name

    def getValue(self) -> str | float:
        return self.__value


class Properties:
    __properties: list[Property]

    def __init__(self, *properties: Property):
        self.__properties: List[Property] = list(properties)

    def __str__(self) -> str:
        return "{" + ", ".join(
            [f"{property.getName()}: '{property.getValue()}'" for property in self.__properties]) + "}"

    def getListProperties(self) -> List[Property]:
        return self.__properties


class CategoryNode:
    __name: str

    def __init__(self, name: str):
        self.__name = name.capitalize()

    def getName(self) -> str:
        return self.__name

    def setName(self, s: str):
        self.__name = s

    def __str__(self) -> str:
        res = f":{self.__name}" if len(self.__name) > 0 else ""
        return res


class CategoryRelation(CategoryNode):
    def __init__(self, name: str):
        super().__init__(name)
        self.setName(StringFunctions.CapitalizeAndRemove_(self.getName()))


class Variable:
    __name: str

    def __init__(self, name: str):
        self.__name = name

    def isEmpty(self) -> bool:
        return self.__name == ''

    def __str__(self) -> str:
        return f"{self.__name}"

    def __eq__(self, other):
        return self.__name == str(other)

    def isExist(self) -> bool:
        return True if len(self.__name) != 0 else False


class BaseNeo4j:

    def __init__(self, category: str = None, variable: str = None, **properties):
        self.__properties: Optional[Properties] = Properties(*[Property(propertiesName, propertiesValue)
                                                               for propertiesName, propertiesValue in
                                                               properties.items()])

        self.__variable: Variable = Variable(variable) if variable else Variable("")
        self.__category: CategoryNode = CategoryNode(category) if category else CategoryNode("")

    def getCategory(self) -> CategoryNode:
        return self.__category

    def getVariable(self) -> Variable:
        return self.__variable

    def getProperties(self) -> Properties:
        return self.__properties

    def getPropertyNode(self) -> List['PropertyNode']:
        return [PropertyNode(self, p) for p in self.getProperties().getListProperties()]


class NodeNeo4j(BaseNeo4j):
    __category: CategoryNode
    __variable: Variable
    __properties: Properties | None

    def __init__(self, category: str = None, variable: str = None, **properties):
        super().__init__(category, variable, **properties)

    def __str__(self) -> str:
        return f"({self.getVariable()}{self.getCategory()} {self.getProperties()})"


class RelationNeo4j(BaseNeo4j):

    def __init__(self, category: str = None, variable: str = None, toRight: bool = False, toLeft: bool = False,
                 **properties):
        super().__init__(category, variable, **properties)

        self.__toRight = False
        self.__toLeft = False
        self.setToRight(toRight)
        self.setToLeft(toLeft)

    def setToRight(self, new: bool) -> None:
        self.__toLeft = False if self.__toLeft is True & new is True else self.__toLeft
        self.__toRight = new

    def setToLeft(self, new: bool) -> None:
        self.__toRight = False if self.__toRight is True & new is True else self.__toRight
        self.__toLeft = new

    def __str__(self):
        if self.__toRight:
            res = f"-[{self.getVariable()}{self.getCategory()} {self.getProperties()}]->"
        elif self.__toLeft:
            res = f"<-[{self.getVariable()}{self.getCategory()} {self.getProperties()}]-"
        else:
            res = f"-[{self.getVariable()}{self.getCategory()} {self.getProperties()}]-"
        return res


class PropertyNode:
    def __init__(self, node: NodeNeo4j | RelationNeo4j, prop: Property | str):
        propStr: str = prop if isinstance(prop, str) else prop.getName()
        requireProp: List[Property] = [p for p in node.getProperties().getListProperties() if p.getName() == propStr]

        self.__node: NodeNeo4j | RelationNeo4j = node

        if len(requireProp) == 0:
            raise QuerryException(f'{propStr} is not part of the Node: {node}', level=1)
        elif self.__node.getVariable().isExist() is False:
            raise QuerryException(f'Property {propStr} need variable in node: {self.__node}')
        else:
            self.__name: str = propStr
            self.__value: str | float = requireProp[0].getValue()

    def getVariable(self) -> Variable:
        return self.__node.getVariable()

    def __str__(self) -> str:
        if self.__node.getVariable().isExist() is False:
            raise QuerryException(f'Property {self.__name} need variable in node: {self.__node}')
        return f'{self.__node.getVariable()}.{self.__name}={self.__value}'

    def getValue(self) -> str | float:
        return self.__value

    def getName(self) -> str:
        return f"{self.__node.getVariable()}.{self.__name}"


class PatternQuerry:

    def __init__(self, *elements: RelationNeo4j | NodeNeo4j):

        self.__elements: List[RelationNeo4j | NodeNeo4j] = [*elements]

        if not all([isinstance(n, (type(None), NodeNeo4j, RelationNeo4j)) for n in self.__elements]):
            notAccepted = [n.__name__ for n in self.__elements if
                           not isinstance(n, (type(None), NodeNeo4j, RelationNeo4j))]
            raise QuerryException(f'Type Error of the input in the pattern, is not accepted: {notAccepted}', level=1)

    def getElements(self) -> List[RelationNeo4j | NodeNeo4j]:
        return self.__elements

    def getProperty(self, n: NodeNeo4j, p: str | Property) -> PropertyNode:
        if n not in self.getNodes(): raise QuerryException(f'{str(n)} in not part of {self}', level=1)
        return PropertyNode(n, p)

    def getNodes(self) -> List[NodeNeo4j]:
        return [element for element in self.__elements if isinstance(element, NodeNeo4j)]

    def getPropertiesNodeList(self) -> List[Property]:
        return ListUtils(
            [ps.getListProperties() for ps in [node.getProperties() for node in self.getNodes()]]).flatLists()

    def getAllVariables(self) -> List[Variable]:
        return [element.getVariable() for element in self.__elements]

    def getPropertyNode(self) -> List[PropertyNode]:
        return ListUtils([n.getPropertyNode() for n in self.getElements()]).flatLists()

    def __str__(self):
        return ''.join([str(element) for element in self.__elements])


class Expression(str):
    def __init__(self, s):
        super(Expression, self).__init__(s)


class PatternSet:
    def __init__(self, leftMember: PropertyNode, rightMember: Union[str | int | float | Expression]):
        self.__right: str | float = rightMember if isinstance(rightMember, str) else FiguresFunctions.convertInFloat(
            rightMember)
        self.__leftMember: PropertyNode = leftMember

    def __str__(self) -> str:
        return f"{self.__leftMember.getName()} = {self.__right}"


if __name__ == '__main__':
    a = NodeNeo4j('personne', age=12, sexe='f')
    b = RelationNeo4j('lien de parente', taille=12, toLeft=True, variable='b')
    c = NodeNeo4j('annimal', sexe='m')
    f = (PatternQuerry(a, b, c))

    g = PropertyNode(a, "age")
    pass
