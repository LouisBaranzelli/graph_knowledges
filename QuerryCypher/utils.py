import itertools
from typing import List


class StringFunctions:

    def __init__(self):
        pass

    @staticmethod
    def CapitalizeAndRemove_(s: str) -> str:
        return s.upper().replace(' ', '_')


class FiguresFunctions:

    def __init__(self):
        pass

    @staticmethod
    def convertInFloat(f: int | float) -> float:
        return float(f)


class ListUtils(List):

    def __init__(self, l: List):
        super().__init__(l)

    def flatLists(self) -> 'ListUtils':
        '''
        [1, [2, 3], 4, 5] =-> [1, 2, 3, 4, 5]
        '''
        return ListUtils(itertools.chain.from_iterable([item] if not isinstance(item, list) else item for item in self))

    def removeNone(self) -> 'ListUtils':
        '''
        [1, None, 4, 5] =-> [1, 4, 5]
        '''
        return ListUtils([e for e in self if e is not None])

    def isInstance(self, *cl) -> bool:
        '''
        ListUtils([1, 2, '3']).isInstance(int) -> False
        ListUtils([1, 2, '3']).isInstance(int, str) -> true
        '''
        return all([isinstance(e, cl)for e in self])

    def getInstanceOf(self, *cl) -> 'ListUtils':
        '''
         ListUtils([1, 2, '3']).isInstance(int) -> [1, 2]
        '''
        return ListUtils([e for e in self if isinstance(e, cl)])


if __name__ == "__main__":
    print(ListUtils([1, 2, '3']).getInstanceOf(int))
