
from typing import List

import neo4j
from neo4j import GraphDatabase, Result

from src.common.LogService import LogService, LogLevel


class DriverNeo4j:
    __instance: 'DriverNeo4j' = None

    def __init__(self, uri=f"bolt://localhost:7687", user="neo4j", password="12345678", database='development'):
        auth = neo4j.Auth("basic", user, password)
        self.__driver = GraphDatabase.driver(uri, auth=auth)
        self.__database: str = database
        self.__driver.verify_connectivity()

        if database == 'test': # in case test: clean all
            self.send('MATCH (n) DETACH DELETE n;')

    def send(self, querry: str) -> List:
        session = self.__driver.session(database=self.__database)
        try:
            LogService().write(querry, level=LogLevel.DEBUG)
            return session.run(querry).values()
        finally:
            session.close()

    def close(self):
        self.__driver.close()
        DriverNeo4j.__instance = None

    @staticmethod
    def getInstance() -> 'DriverNeo4j':
        return DriverNeo4j.__instance

    @staticmethod
    def instanceReset():
        DriverNeo4j.__instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
