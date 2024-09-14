import pytest

from dataStructure.Level import TimeCycle, Level
from dataStructure.NodeQuerryManager import NodeQuerryManager
from src.QuerryCypher.PatternQuerry import NodeNeo4j
from src.common.TimeService import TimeNeo4j
from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException
from src.neo4j.dataStructure.RelationQuerryManager import RelationQuerryManager


class TestRelation:

    def test_get_modify_querry(self):
        relation = RelationQuerryManager(hashValue='toto', name='Louis', fromCategory=['person'], toCategory=['person'])
        assert relation.getModifyQuerry(propertyName='name',
                                        newValue='Pierre') == "MATCH ()-[r:INFORMATION{hash: 'toto'}]-()\nSET r.name='Pierre'"

        with pytest.raises(DataStructureArgumentException):
            relation.getModifyQuerry(propertyName='hashValue', newValue='pierre')
        with pytest.raises(DataStructureArgumentException):
            relation.getModifyQuerry(propertyName='means_no_thing', newValue='pierre')

    def test_getItem(self):
        RelationQuerryManager.getItemQuerry(fromNodeHash='toto', toNodeHash='tata')
        assert RelationQuerryManager.getItemQuerry(fromNodeHash='toto',
                                                   toNodeHash='tata') == "MATCH (n1{hashValue: 'toto'})-[r:INFORMATION]-(n2{hashValue: 'tata'})\nRETURN r"
        assert RelationQuerryManager.getItemQuerry(
            fromNodeHash='toto') == "MATCH (n1{hashValue: 'toto'})-[r:INFORMATION]-(n2)\nRETURN r"
        assert RelationQuerryManager.getItemQuerry() == "MATCH (n1)-[r:INFORMATION]-(n2)\nRETURN r"
        assert RelationQuerryManager.getItemQuerry(hashValue='titi') == "MATCH (n1)-[r:INFORMATION{hashValue: 'titi'}]-(n2)\nRETURN r"
        assert RelationQuerryManager.getItemQuerry(hashValue='titi',
                                                   name='louis') == "MATCH (n1)-[r:INFORMATION{hashValue: 'titi', name: 'louis'}]-(n2)\nRETURN r"
        assert RelationQuerryManager.getItemQuerry(hashValue='titi',
                                                   fromCategory=['chien', 'chat'],
                                                   name='louis') == "MATCH (n1:Chien:Chat)-[r:INFORMATION{hashValue: 'titi', name: 'louis'}]-(n2)\nRETURN r"
        assert RelationQuerryManager.getItemQuerry(hashValue='titi',
                                                   fromCategory=['chien', 'chat'],
                                                   toCategory=['renard'],
                                                   toNodeHash='coco',
                                                   name='louis') == "MATCH (n1:Chien:Chat)-[r:INFORMATION{hashValue: 'titi', name: 'louis'}]-(n2:Renard{hashValue: 'coco'})\nRETURN r"

    def test_create(self):
        r = RelationQuerryManager(name='louis', level=1, message='nouvelle relation', fromCategory=['person'],
                                  toCategory=['person'], hashValue='loulou')
        n1 = NodeQuerryManager(hashValue='toto', category='person', name='harry')
        n2 = NodeQuerryManager(hashValue='titi', category='person', name='jean')
        uptimeStr = TimeCycle().getNextStep(Level(1)).toString()
        assert r.getCreateQuerry(fromNode=n1,
                                 toNode=n2) == "MATCH (n1{hashValue: 'toto'}), (n2{hashValue: 'titi'})\nMERGE (n1)-[r:INFORMATION{name: 'louis', message: 'nouvelle relation', hashValue: 'loulou', date_creation: '" + TimeNeo4j.getNow().toString() + "', level: 1.0, update: '" + uptimeStr + "'}]->(n2)"
        n1 = NodeQuerryManager(hashValue='toto', category='chien', name='harry')
        with pytest.raises(DataStructureArgumentException):
            r.getCreateQuerry(fromNode=n1, toNode=n2)
        n1 = NodeQuerryManager(hashValue='toto', category='person', name='harry')
        n2 = NodeQuerryManager(hashValue='titi', category='chat', name='jean')
        with pytest.raises(DataStructureArgumentException):
            r.getCreateQuerry(fromNode=n1, toNode=n2)



    def test_delete(self):
        r = RelationQuerryManager(name='louis', level=1, message='nouvelle relation', fromCategory=['person'],
                                  toCategory=['persom'], hashValue='loulou')
        n1 = NodeQuerryManager(hashValue='titi', category='person', name='harry')
        n2 = NodeQuerryManager(hashValue='toto', category='person', name='jean')
        assert r.getDeleteQuerry(
            fromNode=n1, toNode=n2) == "MATCH (n1{hashValue: 'titi'})-[r:INFORMATION{hashValue: 'loulou'}]-(n2{hashValue: 'toto'})\nDELETE r"
