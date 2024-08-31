from datetime import datetime, timedelta

from src.common.LogService import LogService, LogLevel


class TimeNeo4j():
    __format = None  # '%d/%m/%Y'

    def __init__(self, year: int = 0, month: int = 0, day: int = 0, hour: int = 0, minute: int = 0, timeFormat: str = None):
        self.__time: datetime = datetime(year, month, day, hour, minute)

    @staticmethod
    def getNow() -> 'TimeNeo4j':
        return TimeNeo4j(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute)

    def addDay(self, d: int) -> 'TimeNeo4j':
        delta = timedelta(days=d)
        newTime = self.__time + delta
        return TimeNeo4j(newTime.year, newTime.month, newTime.day)


    def toString(self) -> str:
        return self.__time.strftime(TimeNeo4j.__format)

    def __new__(cls, year: int = 0, month: int = 0, day: int = 0, hour: int = 0, minute: int = 0, timeFormat: str = '%d/%m/%Y'):
        if TimeNeo4j.__format is None:
            TimeNeo4j.__format = timeFormat
            LogService().write(f"Date format: {cls.__format}.", level=LogLevel.INFO)
        return super().__new__(cls)
