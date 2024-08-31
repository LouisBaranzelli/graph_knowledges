import pytest

from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException
from src.neo4j.dataStructure.Relation import Relation

def test_get_all_relation():
    assert Relation.getAllQuerry() == "MATCH ()-[r]-()\nRETURN r"
    assert Relation.getAllQuerry(['Personne', 'annimal']) == "MATCH ()-[r:Personne:Annimal]-()\nRETURN r"
    assert Relation.getAllQuerry(['Personne', 'annimal'], fromCategory=['Group'], toCategory=['region', 'espece']) == "MATCH (:Group)-[r:Personne:Annimal]->(:Region:Espece)\nRETURN r"


def test_get_modify_querry():
    relation = Relation(fromCategory='personne', toCategory='etudiant', hash = 'toto', name='Louis')
    assert relation.getModifyQuerry(propertyName='name', newValue='Pierre') == "MATCH ()-[r{hash: 'toto'}]-()\nSET r.name = 'Pierre'"

    with pytest.raises(DataStructureArgumentException):
        relation.getModifyQuerry(propertyName='hashValue', newValue='pierre')
    with pytest.raises(DataStructureArgumentException):
        relation.getModifyQuerry(propertyName='means_no_thing', newValue='pierre')