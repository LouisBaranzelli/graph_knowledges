from common.ErrorService import ErrorService
from common.LogService import LogService, LogLevel
from neo4j.dataStructure.Node import Node
from neo4j.dataStructure.Relation import Relation
from neo4j.dataStructure.NodesRelation import NodesRelation
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Main:


    def __init__(self):

        self.error_service: ErrorService = None
        self.logger: LogService = None

        self.initialize()
        self.logger.info("Demmarage")

        try:

            relation = Relation('louis', ['Personne', 'animal'], ['Personnes'])
            node1 = Node('louis', ['Personne', 'ANimal'])
            node2 = Node('louis', 'Personne')
            a = NodesRelation(node1, relation, node2)





        except Exception as e:
            self.error_service.onError(e)

    def initialize(self):
        self.error_service = ErrorService()
        self.logger = LogService()
        self.error_service.addCallback(self.logger.callbackLogException)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
