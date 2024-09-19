import pytest

from datetime import datetime

from src.common.TimeService import TimeNeo4j


def test_time_neo4j():

    assert isinstance(TimeNeo4j.getNow(), TimeNeo4j)
    assert isinstance(TimeNeo4j.getNow().toString(), str)
    assert TimeNeo4j(2023, 1, 1, 0, 0).toString() == "01/01/2023"
    assert TimeNeo4j(2023, 1, 1).addDay(10).toString() == "11/01/2023"
    assert TimeNeo4j.fromString("01/01/2023").toString() == "01/01/2023"
