import pytest

from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException
from src.neo4j.dataStructure.NodeQuerryManager import NodeQuerryManager


def test_get_create_querry():
    node = NodeQuerryManager(name='louis', category=['personne', 'garCon'], hashValue='testhash', message='message')
    assert node.getCreateQuerry() == "MERGE (n:Personne:Garcon{hash: 'testhash'})\nON CREATE SET n.name='louis',n.message='message',n.date_creation='" + node.getDateCreation().toString() + "'"

    node = NodeQuerryManager(name="1", category=[], hashValue='testhash', message='message')
    assert node.getCreateQuerry() == "MERGE (n{hash: 'testhash'})\nON CREATE SET n.name='1',n.message='message',n.date_creation='" + node.getDateCreation().toString() + "'"

def test_get_item_Querry():
    assert NodeQuerryManager.getItemQuerry() == 'MATCH (n)\nRETURN n'
    assert NodeQuerryManager.getItemQuerry(category=['personne'], name='louis',
                                           hashValue='testhash') == "MATCH (n:Personne{name: 'louis', hashValue: 'testhash'})\nRETURN n"


def test_get_set_querry():
    node = NodeQuerryManager(name='louis', category=['personne'], hashValue='testhash', message='message')
    assert node.getModifyQuerry(propertyName='name',
                                newValue='pierre') == "MATCH (n{hash: 'testhash'})\nSET n.name='pierre'\nRETURN n"
    with pytest.raises(DataStructureArgumentException):
        node.getModifyQuerry(propertyName='hashValue', newValue='pierre')
    with pytest.raises(DataStructureArgumentException):
        node.getModifyQuerry(propertyName='means_no_thing', newValue='pierre')



def test_get_delete_querry():
    node = NodeQuerryManager(name='louis', category=['personne'], hashValue='testhash', message='message')
    assert node.getDeleteQuerry() == "MATCH (n:Personne{hash: 'testhash'})\nDELETE n"
