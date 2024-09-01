import pytest

from dataStructure.Level import TimeCycle, Level
from dataStructure.NodeApplication import NodeApplication
from src.QuerryCypher.PatternQuerry import NodeNeo4j
from src.common.TimeService import TimeNeo4j
from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException
from src.neo4j.dataStructure.RelationApplication import RelationApplication


class TestRelation:

    def test_get_modify_querry(self):
        relation = RelationApplication(hashValue='toto', name='Louis', fromCategory=['person'], toCategory=['persom'])
        assert relation.getModifyQuerry(propertyName='name',
                                        newValue='Pierre') == "MATCH ()-[r{hash: 'toto'}]-()\nSET r.name = 'Pierre'"

        with pytest.raises(DataStructureArgumentException):
            relation.getModifyQuerry(propertyName='hashValue', newValue='pierre')
        with pytest.raises(DataStructureArgumentException):
            relation.getModifyQuerry(propertyName='means_no_thing', newValue='pierre')

    def test_getItem(self):
        RelationApplication.getItemQuerry(fromNodeHash='toto', toNodeHash='tata')
        assert RelationApplication.getItemQuerry(fromNodeHash='toto',
                                                 toNodeHash='tata') == "MATCH (n1{hashValue: 'toto'})-[r]-(n2{hashValue: 'tata'})\nRETURN r"
        assert RelationApplication.getItemQuerry(
            fromNodeHash='toto') == "MATCH (n1{hashValue: 'toto'})-[r]-(n2)\nRETURN r"
        assert RelationApplication.getItemQuerry() == "MATCH (n1)-[r]-(n2)\nRETURN r"
        assert RelationApplication.getItemQuerry(hashValue='titi') == "MATCH (n1)-[r{hashValue: 'titi'}]-(n2)\nRETURN r"
        assert RelationApplication.getItemQuerry(hashValue='titi',
                                                 name='louis') == "MATCH (n1)-[r{hashValue: 'titi', name: 'louis'}]-(n2)\nRETURN r"
        assert RelationApplication.getItemQuerry(hashValue='titi',
                                                 fromCategory=['chien', 'chat'],
                                                 name='louis') == "MATCH (n1:Chien:Chat)-[r{hashValue: 'titi', name: 'louis'}]-(n2)\nRETURN r"
        assert RelationApplication.getItemQuerry(hashValue='titi',
                                                 fromCategory=['chien', 'chat'],
                                                 toCategory=['renard'],
                                                 toNodeHash='coco',
                                                 name='louis') == "MATCH (n1:Chien:Chat)-[r{hashValue: 'titi', name: 'louis'}]-(n2:Renard{hashValue: 'coco'})\nRETURN r"

    def test_create(self):
        r = RelationApplication(name='louis', level=1, message='nouvelle relation', fromCategory=['person'], toCategory=['persom'], hashValue='loulou')
        n1 = NodeApplication(hashValue='toto', category='person', name='harry')
        n2 = NodeApplication(hashValue='titi', category='person', name='jean')
        uptimeStr = TimeCycle().getNextStep(Level(1)).toString()
        assert r.getCreateQuerry(fromNode=n1,
                                 toNode=n2) == "MATCH (n1{hashValue: 'toto'}), (n2{hashValue: 'titi'})\nCREATE (n1)-[r{name: 'louis', message: 'nouvelle relation', hashValue: 'loulou', date_creation: '" + TimeNeo4j.getNow().toString() + "', level: 1.0, update: '" + uptimeStr + "'}]->(n2)"
