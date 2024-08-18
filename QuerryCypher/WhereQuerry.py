from typing import Type, List, Union, Optional
from utils import FiguresFunctions, ListUtils
from CypherException import QuerryException, TypeException
from PatternQuerry import PatternQuerry, PropertyNode
from enum import Enum


class CypherWhereOperator(Enum):
    # Opérateurs de comparaison
    EQUAL = ('=', float)
    NOT_EQUAL = ('<>', float)
    NOT_EQUAL_ALT = ('!=', float)
    LESS_THAN = ('<', float)
    GREATER_THAN = ('>', float)
    LESS_THAN_OR_EQUAL = ('<=', float)
    GREATER_THAN_OR_EQUAL = ('>=', float)

    # # Opérateurs logiques
    # AND = 'AND'
    # OR = 'OR'
    # NOT = 'NOT'

    # Opérateurs de chaîne
    STARTS_WITH = ('STARTS WITH', str)
    ENDS_WITH = ('ENDS WITH', str)
    CONTAINS = ('CONTAINS', str)

    # # Opérateurs de vérification de nullité
    # IS_NULL = 'IS NULL'
    # IS_NOT_NULL = 'IS NOT NULL'

    # # Opérateurs d'existence de pattern
    # EXISTS = 'EXISTS'

    def __new__(cls, symbole, valueType):
        obj: Enum = object.__new__(cls)
        obj.__valueType = valueType  # type class
        obj.__symbole = symbole  # type str
        return obj

    def getType(self) -> Type:
        return self.__valueType

    def getValue(self) -> str:
        return self.__symbole


class ConditionalPattern:

    def __init__(self, leftValue: PropertyNode, operator: CypherWhereOperator, rightValue: float | int | str):

        rightValue: str | float = rightValue if isinstance(rightValue, str) else FiguresFunctions.convertInFloat(
            rightValue)
        if not isinstance(leftValue.getValue(), operator.getType()):
            raise QuerryException(
                f'Wrong left-hand operator type: {operator.getValue()} needs {operator.getType()}, got: {type(leftValue.getValue())}',
                level=1)
        if not isinstance(rightValue, operator.getType()):
            raise QuerryException(
                f'Wrong left-hand operator type: {operator.getValue()} needs float|int|str, got: {type(rightValue.getValue())}',
                level=1)
        self.__leftValue: PropertyNode = leftValue
        self.__rightValue: float | str = rightValue
        self.__operator: str = operator.getValue()

    def __str__(self) -> str:
        return f"{str(self.__leftValue.getName())}{self.__operator}{self.__rightValue}"

    def getPropertyNode(self) -> PropertyNode:
        return self.__leftValue


class CommonWhere:
    def __init__(self, *values: Union['WherePattern', 'AndPattern', PatternQuerry, ConditionalPattern]):
        for value in values:
            if not isinstance(value, (AndPattern, OrPattern, PatternQuerry, ConditionalPattern)):
                raise TypeException(
                    f'{str(value)} ({value.__class__.__name__}) not accepted in {self.__class__.__name__} only [AndPattern|WherePattern|PatternQuerry|ConditionalPattern]')

        self.__values: List[Union[OrPattern, AndPattern, PatternQuerry, ConditionalPattern]] = list(values)

    def getValues(self) -> List[Union['AndPattern', 'OrPattern', PatternQuerry, ConditionalPattern]]:
        return self.__values

    def getAllConditionalPattern(self) -> List[Union['AndPattern', 'OrPattern', PatternQuerry, ConditionalPattern]]:
        lOrNAnd = [e.getAllConditionalPattern() for e in
                   ListUtils(self.__values).getInstanceOf(AndPattern, OrPattern)]
        lQuerryNConditionalPat = [e for e in ListUtils(self.__values).getInstanceOf(PatternQuerry, ConditionalPattern)]
        return lOrNAnd + lQuerryNConditionalPat


class OrPattern(CommonWhere):
    def __init__(self, *values: Union['WherePattern', 'AndPattern', PatternQuerry, ConditionalPattern]):
        super().__init__(*values)

    def __str__(self) -> str:
        return '(' + " OR ".join([str(value) for value in self.getValues()]) + ')'


class AndPattern(CommonWhere):

    def __init__(self, *values: Union[OrPattern, 'AndPattern', PatternQuerry, ConditionalPattern]):
        super().__init__(*values)

    def __str__(self) -> str:
        return '(' + " AND ".join([str(value) for value in self.getValues()]) + ')'


class WhereQuerry(CommonWhere):
    def __init__(self, *values: Union[OrPattern, 'AndPattern', PatternQuerry, ConditionalPattern]):
        super().__init__(*values)

        if len(values) > 1:
            for value in values:
                if not isinstance(value, (AndPattern, OrPattern)):
                    raise TypeException(
                        f'{str(value)} ({value.__class__.__name__}) not accepted in {self.__class__.__name__} only [AndPattern|WherePattern] if more than 1 pattern used [[AndPattern|WherePattern|PatternQuerry|ConditionalPattern]]')

    def __str__(self) -> str:
        return '(' + "".join([str(value) for value in self.getValues()]) + ')'
