import pytest
from pathlib import Path
from src.common.ConfigService import ConfigService, Parameter
from src.utils.Constant import ROOT_DIR


def test_ConfigService():
    try:
        configService = ConfigService()
    except Exception as e:
        pytest.fail(f"An exception was raised: {e}, \nRoot Path: {ROOT_DIR}")

    configService.reset()
    testConfigPath: str = str((Path(__file__).parent / "test_config.json").resolve())
    configService = ConfigService(pathConfig=testConfigPath)
    assert configService.getUserConfig().getLevelMax() == 8
    assert configService.getUserConfig().getLearningCycle() == 180

def test_Parameter():
    parameter = Parameter(value=5, classAutorized=int, max=6, min=3)
    assert parameter.set(4) == True
    assert parameter.set(7) == False
    assert parameter.get() == 6
    assert parameter.set(2) == False
    assert parameter.get() ==3
    assert parameter.set('test') == False

    parameter = Parameter(value='Pierre', classAutorized=str)
    assert parameter.set(1) == False
    assert parameter.set('Louis') == True
    assert parameter.get() == 'Louis'


