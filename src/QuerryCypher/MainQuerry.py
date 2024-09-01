from typing import List
from src.QuerryCypher.CypherException import QuerryException
from src.QuerryCypher.WhereQuerry import WhereQuerry, ConditionalPattern
from src.QuerryCypher.PatternQuerry import NodeNeo4j, PatternQuerry, Variable, PropertyNode, PatternSet
from src.QuerryCypher.utils import ListUtils


class CreateQuerry:

    def __init__(self, value: [PatternQuerry | NodeNeo4j]):
        self.__value: [PatternQuerry | NodeNeo4j] = value

    def __str__(self) -> str:
        return f"CREATE {str(self.__value)}"


class MatchQuerry:

    def __init__(self, inputs: List[PatternQuerry | NodeNeo4j], outputs: List[Variable | PropertyNode] = [], where: WhereQuerry = None):

        self.__inputs: [PatternQuerry | NodeNeo4j] = inputs
        self.__where: WhereQuerry = where
        self.__outputs: List[Variable | PropertyNode] = outputs

        if not ListUtils(inputs).isInstance(PatternQuerry, NodeNeo4j):
            raise (QuerryException(f"Only PatternQuerry and NodeNeo4j accepted in input"))
        if not ListUtils(outputs).isInstance(Variable, PropertyNode):
            raise (QuerryException(f"Only Variable and PropertyNode accepted in output"))

        if where is not None:
            elementWhere: List[PatternQuerry, ConditionalPattern] = where.getAllConditionalPattern()
            listVarWhere: List[Variable] = [el.getVariable() for el in ListUtils([e.getPropertyNode() for e in elementWhere]).flatLists()]
            listVarInput: List[Variable] = [el.getVariable() for el in ListUtils([e.getPropertyNode() for e in inputs]).flatLists()]
            if not all([w in listVarInput for w in listVarWhere]):
                raise (QuerryException(f"Variables in where condition: {[str(s) for s in listVarWhere]} must be in input variables: {[str(s) for s in listVarInput]}."))

        variablesListInput: ListUtils[Variable]
        v1: List = [e.getVariable() for e in ListUtils(inputs).getInstanceOf(NodeNeo4j)]
        v2: List = [e.getAllVariables() for e in ListUtils(inputs).getInstanceOf(PatternQuerry)]
        variablesListInput = ListUtils(v1 + v2). flatLists().removeNone()
        testVariable: List[bool] = [variable in variablesListInput and variable.isExist() for variable in ListUtils(outputs).getInstanceOf(Variable)]

        if not all(testVariable):
            raise (QuerryException(f"At least one required Variable in output : {[str(v) for v in ListUtils(outputs).getInstanceOf(Variable)]} not in the input: {[str(v) for v in variablesListInput]} "))

    def getInputs(self) -> [PatternQuerry | NodeNeo4j]:
        return self.__inputs

    def getWhere(self) -> WhereQuerry:
        return self.__where

    def getOutputs(self) -> List[Variable | PropertyNode]:
        return self.__outputs

    def __str__(self) -> str:
        match: str = f"MATCH {', '.join([str(e) for e in self.__inputs])}\n"
        where: str = f"WHERE({str(self.__where)})\n" if self.__where is not None else ""
        ret: str = f"RETURN {', '.join([str(e.getName()) for e in self.__outputs])}" if len(self.__outputs) != 0 else ""
        return f"{match}{where}{ret}"


class SetQuerry(MatchQuerry):
    def __init__(self, inputs: List[PatternQuerry | NodeNeo4j], setValue: PatternSet, outputs: List[Variable | PropertyNode] = [], where: WhereQuerry = None):
        super().__init__(inputs, outputs, where)
        self.__set: PatternSet = setValue
        if not isinstance(setValue, PatternSet):
            raise (QuerryException(f"Type error for set querry, got: : {type(setValue)}."))

    def __str__(self) -> str:
        match: str = f"MATCH {', '.join([str(e) for e in self.getInputs()])}\n"
        where: str = f"WHERE{str(self.getWhere())}\n" if self.getWhere() is not None else ""
        setValue: str = f"SET {str(self.__set)}"
        ret: str = f"\nRETURN {', '.join([str(e.getName()) for e in self.getOutputs()])}" if len(self.getOutputs()) != 0 else ""
        return f"{match}{where}{setValue}{ret}"


class DeleteQuerry(MatchQuerry):
    def __init__(self, inputs: List[PatternQuerry | NodeNeo4j], outputs: List[Variable], where: WhereQuerry = None):
        super().__init__(inputs, outputs,where)
        if not ListUtils(outputs).isInstance(Variable):
            raise (QuerryException(f"Only Variable accepted in output"))

    def __str__(self) -> str:
        match: str = f"MATCH {', '.join([str(e) for e in self.getInputs()])}\n"
        where: str = f"WHERE{str(self.getWhere())}\n" if self.getWhere() is not None else ""
        ret: str = f"DELETE {', '.join([str(e) for e in self.getOutputs()])}"
        return f"{match}{where}{ret}"

if __name__ == '__main__':
    pass

# gerer les modify
# faire les testes
