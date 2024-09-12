import pytest

from communication.Node import Node
from communication.ServerService import DriverNeo4j
from dataStructure.Neo4jError import DataBaseLogicException
from src.common.TimeService import TimeNeo4j


class TestNode:
    DriverNeo4j.instanceReset()
    DriverNeo4j(database='test')

    @pytest.fixture
    def nodeAFixture(self):
        return Node(name="John", hashValue='bonbon', category=['personne', 'employeur'],
                    message='Est le directeur de la station',
                    driver=DriverNeo4j.getInstance())

    @pytest.fixture
    def nodeBFixture(self):
        return Node(name="Jean", category=['personne', 'responsable'], message='Est le responsable de la station',
                    hashValue='code_non_unique',
                    driver=DriverNeo4j.getInstance())

    @pytest.fixture
    def nodeCFixture(self):
        return Node(name="Jean", category=['responsable', 'personne'], message='Est le responsable de la station',
                    driver=DriverNeo4j.getInstance())

    @pytest.fixture
    def nodeDFixture(self):
        return Node(name="Jean", category=['Ami'], message='',
                    driver=DriverNeo4j.getInstance())

    def test_getItem(self, nodeAFixture, nodeBFixture, nodeCFixture):
        assert len(Node.getItem(category=['Employeur'], driver=DriverNeo4j.getInstance())) == 0
        nodeAFixture.create()
        assert len(Node.getItem(category=['employeuR'], driver=DriverNeo4j.getInstance())) == 1

        node: Node = Node.getItem(name='John', driver=DriverNeo4j.getInstance())[0]
        assert node.getName() == 'John'
        assert node.getCategory() == ['Personne', 'Employeur'] or ['Employeur', 'Personne']
        assert node.getMessage() == 'Est le directeur de la station'
        assert node.getHashValue() == 'bonbon'
        assert node.getTimeCreation().toString() == TimeNeo4j.getNow().toString()

        nodeBFixture.create()
        assert len(Node.getItem(category=['personne'], driver=DriverNeo4j.getInstance())) == 2

    def test_isExist(self, nodeAFixture, nodeCFixture):
        assert nodeAFixture.isExist()
        assert nodeCFixture.isExist() is False

    def test_creation(self, nodeAFixture, nodeBFixture, nodeCFixture):
        DriverNeo4j.instanceReset()
        DriverNeo4j(database='test')

        assert len(Node.getItem(driver=DriverNeo4j.getInstance())) == 0

        nodeAFixture.create()
        assert len(Node.getItem(driver=DriverNeo4j.getInstance())) == 1

        nodeBFixture.create()
        assert len(Node.getItem(driver=DriverNeo4j.getInstance())) == 2

        with pytest.raises(DataBaseLogicException):
            nodeBFixture.create()  # create a node with an existing hash shouldn't work

        nodeCFixture.create()  # create similar but with a different hash
        assert len(Node.getItem(driver=DriverNeo4j.getInstance())) == 3

    def test_modify(self, nodeDFixture):

        with pytest.raises(DataBaseLogicException): # Impossible modify unexisting Node
            nodeDFixture.modify('name', 'pierre')
        node: Node = Node.getItem(name='John', driver=DriverNeo4j.getInstance())[0]
        nodeModified: Node = node.modify('name', 'Louis')
        nodeModified = nodeModified.modify('message', 'nouveau message')
        assert nodeModified.getName() == 'Louis'
        assert nodeModified.getMessage() == 'nouveau message'
        assert len(Node.getItem(name='John', driver=DriverNeo4j.getInstance())) == 0
        assert len(Node.getItem(name='Louis', driver=DriverNeo4j.getInstance())) == 1

        # Use an existing hash but with different name to create doesn't work
        with pytest.raises(DataBaseLogicException):
            node.create() # shouldn't work because hash existing'
        assert len(Node.getItem(driver=DriverNeo4j.getInstance())) == 3
        assert len(Node.getItem(name='Louis', driver=DriverNeo4j.getInstance())) == 1
        assert len(Node.getItem(name='John', driver=DriverNeo4j.getInstance())) == 0

    def test_delete(self):
        node: Node = Node.getItem(name='Louis', driver=DriverNeo4j.getInstance())[0]
        node.delete()
        assert node.isExist() is False
        with pytest.raises(DataBaseLogicException): # Can not delete unexistind node
            node.delete()
