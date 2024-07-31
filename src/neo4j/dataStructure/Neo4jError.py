from src.common.LogService import LogService, LogLevel

from typing import List
from src.neo4j.dataStructure.BaseStructure import BaseStructure


class Neo4jError(Exception):
    """Base class for exceptions in this application."""
    pass


class DataStructureException(Neo4jError):
    def __init__(self, elements: List[List[BaseStructure]],  message: str):
        messages: list[str] = []
        [messages.append("["+' ,'.join([element_ for element_ in element])+"]") for element in elements]
        message = f"{' AND '.join(messages)} not Compatible. {message}"
        super().__init__(message)


