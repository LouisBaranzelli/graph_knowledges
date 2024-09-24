import pytest

from communication.Relation import Relation
from communication.ServerService import DriverNeo4j

from dataStructure.NodeQuerryManager import NodeQuerryManager
from src.QuerryCypher.PatternQuerry import NodeNeo4j
from src.common.TimeService import TimeNeo4j
from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException
from src.neo4j.dataStructure.InformationQuerryManager import InformationQuerryManager


class TestRelation:

    @pytest.fixture
    def nodeAFixture(self):
        return NodeQuerryManager(name='Louis', category='Personne', hashValue='titi')

    @pytest.fixture
    def nodeBFixture(self):
        return NodeQuerryManager(name='Lille', category='Ville', hashValue='toto')

    @pytest.fixture
    def nodeCFixture(self):
        return NodeQuerryManager(name='Lille', category='Village', hashValue='toto')

    @pytest.fixture
    def relation(self):
        return Relation(fromCategory=["Personne"], toCategory=['ville'], name='se_deplace',
                                  hashValue='tonton')

    def test_CreateQuerry(self, nodeAFixture, nodeBFixture, nodeCFixture, relation):

        information: InformationQuerryManager = InformationQuerryManager(relation=relation, fromNode=nodeAFixture, toNode=nodeBFixture)
        assert information.getCreateQuerry() == "MATCH (n1{hashValue: 'titi'}), (n2{hashValue: 'toto'})\nMERGE (n1)-[r:INFORMATION{hashValue: 'tonton', date_creation: '" + TimeNeo4j.getNow().toString() + "', level: 0.0, updateTime: '" + TimeNeo4j.getNow().addDay(
            8).toString() + "'}]->(n2)"

        information: InformationQuerryManager = InformationQuerryManager(relation=relation, fromNode=nodeCFixture, toNode=nodeBFixture)
        with pytest.raises(DataStructureArgumentException):
            information.getCreateQuerry()

        information: InformationQuerryManager = InformationQuerryManager(relation=relation, fromNode=nodeAFixture, toNode=nodeCFixture)
        with pytest.raises(DataStructureArgumentException):
            information.getCreateQuerry()

    def test_get_modify_querry(self, relation, nodeAFixture, nodeBFixture):

        information: InformationQuerryManager = InformationQuerryManager(relation=relation, fromNode=nodeAFixture, toNode=nodeBFixture)
        assert information.getModifyQuerry(propertyName='level',
                                           newValue='1') == "MATCH ({hashValue: 'titi'})-[r:INFORMATION]-({hashValue: 'toto'})\nSET r.level='1'"

        with pytest.raises(DataStructureArgumentException):
            information.getModifyQuerry(propertyName='hashValue', newValue='pierre')
        with pytest.raises(DataStructureArgumentException):
            information.getModifyQuerry(propertyName='means_no_thing', newValue='pierre')

    def test_delete(self, relation, nodeAFixture, nodeBFixture):
        information: InformationQuerryManager = InformationQuerryManager(relation=relation, fromNode=nodeAFixture,
                                                                         toNode=nodeBFixture)
        assert information.getDeleteQuerry() == "MATCH (n1{hashValue: 'titi'})-[r:INFORMATION]-(n2{hashValue: 'toto'})\nDELETE r"

    def test_getItem(self, nodeAFixture, nodeBFixture):
        InformationQuerryManager.getItemQuerry(fromNodeHash='toto', toNodeHash='tata')
        assert InformationQuerryManager.getItemQuerry(fromNodeHash='toto', toNodeHash='tata') == "MATCH (n1{hashValue: 'toto'})-[r:INFORMATION]-(n2{hashValue: 'tata'})\nRETURN r"
        assert InformationQuerryManager.getItemQuerry(
            fromNodeHash='toto') == "MATCH (n1{hashValue: 'toto'})-[r:INFORMATION]-(n2)\nRETURN r"
        assert InformationQuerryManager.getItemQuerry() == "MATCH (n1)-[r:INFORMATION]-(n2)\nRETURN r"
