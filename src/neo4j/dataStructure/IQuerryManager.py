from abc import ABC, abstractmethod


class IQuerryManager(ABC):
    @abstractmethod
    def getCreateQuerry(self, **kwargs) -> str:
        pass

    @abstractmethod
    def getDeleteQuerry(self, **kwargs) -> str:
        pass

    @abstractmethod
    def getModifyQuerry(self, **kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def getItemQuerry(**kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def getStaticInstance() -> 'IQuerryManager':
        pass
