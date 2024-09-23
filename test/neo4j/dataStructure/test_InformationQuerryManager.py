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
    # #
    # def test_getItem(self):
    #     InformationQuerryManager.getItemQuerry(fromNodeHash='toto', toNodeHash='tata')
    #     assert InformationQuerryManager.getItemQuerry(fromNodeHash='toto',
    #                                                toNodeHash='tata') == "MATCH (n1{hashValue: 'toto'})-[r:INFORMATION]-(n2{hashValue: 'tata'})\nRETURN r"
    #     assert InformationQuerryManager.getItemQuerry(
    #         fromNodeHash='toto') == "MATCH (n1{hashValue: 'toto'})-[r:INFORMATION]-(n2)\nRETURN r"
    #     assert InformationQuerryManager.getItemQuerry() == "MATCH (n1)-[r:INFORMATION]-(n2)\nRETURN r"
    #     assert InformationQuerryManager.getItemQuerry(hashValue='titi') == "MATCH (n1)-[r:INFORMATION{hashValue: 'titi'}]-(n2)\nRETURN r"
    #     assert InformationQuerryManager.getItemQuerry(hashValue='titi',
    #                                                name='louis') == "MATCH (n1)-[r:INFORMATION{hashValue: 'titi', name: 'louis'}]-(n2)\nRETURN r"
    #     assert InformationQuerryManager.getItemQuerry(hashValue='titi',
    #                                                fromCategory=['chien', 'chat'],
    #                                                name='louis') == "MATCH (n1:Chien:Chat)-[r:INFORMATION{hashValue: 'titi', name: 'louis'}]-(n2)\nRETURN r"
    #     assert InformationQuerryManager.getItemQuerry(hashValue='titi',
    #                                                fromCategory=['chien', 'chat'],
    #                                                toCategory=['renard'],
    #                                                toNodeHash='coco',
    #                                                name='louis') == "MATCH (n1:Chien:Chat)-[r:INFORMATION{hashValue: 'titi', name: 'louis'}]-(n2:Renard{hashValue: 'coco'})\nRETURN r"
    #
    # def test_create(self):
    #     r = InformationQuerryManager(name='louis', level=1, message='nouvelle relation', fromCategory=['person'],
    #                               toCategory=['person'], hashValue='loulou')
    #     n1 = NodeQuerryManager(hashValue='toto', category='person', name='harry')
    #     n2 = NodeQuerryManager(hashValue='titi', category='person', name='jean')
    #     uptimeStr = TimeCycle().getNextStep(Level(1)).toString()
    #     assert r.getCreateQuerry(fromNode=n1,
    #                              toNode=n2) == "MATCH (n1{hashValue: 'toto'}), (n2{hashValue: 'titi'})\nMERGE (n1)-[r:INFORMATION{name: 'louis', message: 'nouvelle relation', hashValue: 'loulou', date_creation: '" + TimeNeo4j.getNow().toString() + "', level: 1.0, update: '" + uptimeStr + "'}]->(n2)"
    #     n1 = NodeQuerryManager(hashValue='toto', category='chien', name='harry')
    #     with pytest.raises(DataStructureArgumentException):
    #         r.getCreateQuerry(fromNode=n1, toNode=n2)
    #     n1 = NodeQuerryManager(hashValue='toto', category='person', name='harry')
    #     n2 = NodeQuerryManager(hashValue='titi', category='chat', name='jean')
    #     with pytest.raises(DataStructureArgumentException):
    #         r.getCreateQuerry(fromNode=n1, toNode=n2)
    #
    #
    #
    # def test_delete(self):
    #     r = InformationQuerryManager(name='louis', level=1, message='nouvelle relation', fromCategory=['person'],
    #                               toCategory=['persom'], hashValue='loulou')
    #     n1 = NodeQuerryManager(hashValue='titi', category='person', name='harry')
    #     n2 = NodeQuerryManager(hashValue='toto', category='person', name='jean')
    #     assert r.getDeleteQuerry(
    #         fromNode=n1, toNode=n2) == "MATCH (n1{hashValue: 'titi'})-[r:INFORMATION{hashValue: 'loulou'}]-(n2{hashValue: 'toto'})\nDELETE r"
