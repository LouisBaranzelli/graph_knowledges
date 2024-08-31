class CypherException(Exception):
    def __init__(self, message: str, level: int = 0):
        super().__init__(message)


class QuerryException(CypherException):
    def __init__(self, message: str, level: int = 0):
        super().__init__(message, level)


class TypeException(CypherException):
    def __init__(self, message: str, level: int = 0):
        super().__init__(message, level)
