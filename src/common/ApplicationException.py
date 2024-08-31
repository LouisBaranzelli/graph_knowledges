class ApplicationException(Exception):
    def __init__(self,message: str, level: int = 0):
        super().__init__(message)
        self.__level: int = level
        self.__message: str = message

    def getMessage(self) -> str:
        return self.__message