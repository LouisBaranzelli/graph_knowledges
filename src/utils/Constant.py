from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.resolve()
CONFIG_PATH = (Path(ROOT_DIR) / 'config.json').resolve()
