import pytest

from src.neo4j.dataStructure.Neo4jError import DataStructureArgumentException
from src.neo4j.dataStructure.Node import Node


def test_get_create_querry():
    node = Node(name='louis', category=['personne', 'garCon'], hashValue='testhash', message='message')
    assert node.getCreateQuerry() == "CREATE (n:Personne:Garcon{name: 'louis', message: 'message', hash: 'testhash', date_creation: '" + node.getTimeCreation().toString() + "', occurrence: 0.0})"

    node = Node(name="1", category=[], hashValue='testhash', message='message')
    assert node.getCreateQuerry() == "CREATE (n{name: '1', message: 'message', hash: 'testhash', date_creation: '" + node.getTimeCreation().toString() + "', occurrence: 0.0})"


def test_get_item_Querry():
    assert Node.getItemQuerry() == 'MATCH (n)\nRETURN n'
    assert Node.getItemQuerry(category=['personne'], name='louis',
                              hashValue='testhash') == "MATCH (n:Personne{name: 'louis', hashValue: 'testhash'})\nRETURN n"


def test_get_set_querry():
    node = Node(name='louis', category=['personne'], hashValue='testhash', message='message')
    assert node.getModifyQuerry(propertyName='name',
                                newValue='pierre') == "MATCH (n{hash: 'testhash'})\nSET n.name = 'pierre'"
    with pytest.raises(DataStructureArgumentException):
        node.getModifyQuerry(propertyName='hashValue', newValue='pierre')
    with pytest.raises(DataStructureArgumentException):
        node.getModifyQuerry(propertyName='means_no_thing', newValue='pierre')



def test_get_delete_querry():
    node = Node(name='louis', category=['personne'], hashValue='testhash', message='message')
    assert node.getDeleteQuerry() == "MATCH (n:Personne{hash: 'testhash'})\nDELETE n"
