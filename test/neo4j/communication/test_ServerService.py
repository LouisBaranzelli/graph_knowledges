import pytest

from communication.ServerService import DriverNeo4j


class TestDriverNeo4j:

    def test_initialisation_server(self):
        try:
            DriverNeo4j()
        except Exception as e:
            pytest.fail(f"Initialization server failed: {e}")

    def test_reset_server(self):
        DriverNeo4j.instanceReset()
        assert DriverNeo4j.getInstance() is None

        DriverNeo4j.instanceReset()
        DriverNeo4j(database='test')
        assert DriverNeo4j.getInstance() is not None
