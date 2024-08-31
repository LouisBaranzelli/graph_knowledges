from __future__ import annotations
from typing import Optional, Callable, List
import traceback


class ErrorService:
    __instance: Optional[ErrorService] = None

    def __init__(self):
        self.__callbacks: List[Callable[[Exception], None]] = []

    def addCallback(self, callback: Callable[[Exception], None]):
        self.__callbacks.append(callback)

    def delCallback(self, callback: Callable[[Exception], None]):
        if callback in self.__callbacks:
            self.__callbacks.remove(callback)

    def onError(self, error: Exception):
        for callback in self.__callbacks:
            callback(error)
        traceback.print_exc()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance



