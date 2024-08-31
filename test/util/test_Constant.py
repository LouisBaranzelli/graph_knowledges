import pytest
from pathlib import Path
from src.utils.Constant import CONFIG_PATH, ROOT_DIR


def test_Constant():
    assert Path(ROOT_DIR).is_dir(), "Wrong dir root"
    assert Path(CONFIG_PATH).is_file(), "No config file found"

