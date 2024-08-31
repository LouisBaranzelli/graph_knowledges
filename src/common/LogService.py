from __future__ import annotations
from typing import Optional
from pathlib import Path
from loguru import logger
from enum import Enum
import sys


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class LogService:
    __instance: LogService = None
    __flagInitialized: bool = False

    def __init__(self, path: Optional[Path] = Path.cwd().parent / 'log'):

        if not LogService.__flagInitialized:
            path_log: Path = path
            logger.remove()
            # Ajouter une nouvelle configuration de fichier
            logger.add(path_log,
                       format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
            logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")

            __flagInitialized: bool = True

    def callbackLogException(self, e: Exception):
        self.write(str(e), LogLevel.ERROR)

    def write(self, message: str, level: LogLevel = 'DEBUG'):
        if level == LogLevel.DEBUG:
            logger.debug(message)

        if level == LogLevel.INFO:
            logger.info(message)

        if level == LogLevel.WARNING:
            logger.warning(message)

        if level == LogLevel.ERROR:
            logger.error(message)

        if level == LogLevel.CRITICAL:
            logger.critical(message)

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance


if __name__ == '__main__':
    my_logger = LogService()
    my_logger.write('salut', LogLevel.INFO)
