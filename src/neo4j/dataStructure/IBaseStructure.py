from abc import ABC, abstractmethod


class IBaseStructure(ABC):
    @abstractmethod
    def getCreateQuerry(self, **kwargs) -> str:
        pass

    @abstractmethod
    def getDeleteQuerry(self,  **kwargs)  -> str:
        pass

    @abstractmethod
    def getModifyQuerry(self,  **kwargs) -> str:
        pass

    @abstractmethod
    def getItemQuerry(self, **kwargs)  -> str:
        pass

