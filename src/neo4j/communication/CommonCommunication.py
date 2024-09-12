from abc import ABC, abstractmethod


class IElement(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create(self, **kwargs) -> None:
        pass

    @abstractmethod
    def delete(self, **kwargs) -> None:
        pass

    @abstractmethod
    def modify(self, **kwargs) -> None:
        pass

    @abstractmethod
    def isExist(self) -> bool:
        pass

    @abstractmethod
    def getItem(self, **kwargs) -> 'IElement':
        pass