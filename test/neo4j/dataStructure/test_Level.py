import pytest

from src.common.TimeService import TimeNeo4j
from src.neo4j.dataStructure.Level import Level, TimeCycle


class TestLevel:

    def test_level(self):
        maxLevel = Level().getLevelMax()
        minLevel = Level().getLevelMin()
        assert Level(0).getLevel() == 0
        assert Level(maxLevel + 1).getLevel() == maxLevel
        assert Level(minLevel - 1).getLevel() == minLevel

    def test_up_level(self):
        maxLevel = Level().getLevelMax()
        assert Level(maxLevel - 1).upLevel().getLevel() == maxLevel
        assert Level(maxLevel).upLevel().getLevel() == maxLevel

    def test_down_level(self):
        minLevel = 0
        assert Level(minLevel + 1).downLevel().getLevel() == 0
        assert Level(minLevel).downLevel().getLevel() == 0

    class TestTimeCycle:

        def test_TimeNextLevel(self):
            now = TimeNeo4j.getNow()
            timeCycle = TimeCycle(learningTime=32, learningCoef=2)
            assert now.addDay(32).toString() == timeCycle.getNextStep(Level(level=5, levelMax=5)).toString()
            assert now.addDay(16).toString() == timeCycle.getNextStep(Level(level=4, levelMax=5)).toString() # 32 / 2
            assert now.addDay(8).toString() == timeCycle.getNextStep(Level(level=3, levelMax=5)).toString() # 32 / 2
            assert now.addDay(4).toString() == timeCycle.getNextStep(Level(level=2, levelMax=5)).toString() # 32 / 2
            assert now.addDay(2).toString() == timeCycle.getNextStep(Level(level=1, levelMax=5)).toString() # 32 / 2
            assert now.addDay(1).toString() == timeCycle.getNextStep(Level(level=0, levelMax=5)).toString() # 32 / 2

            timeCycle = TimeCycle(learningTime=32, learningCoef=1.7)
            assert now.addDay(32).toString() == timeCycle.getNextStep(Level(level=5, levelMax=5)).toString()
            assert now.addDay(19).toString() == timeCycle.getNextStep(Level(level=4, levelMax=5)).toString()
            assert now.addDay(12).toString() == timeCycle.getNextStep(Level(level=3, levelMax=5)).toString()

            timeCycle = TimeCycle(learningTime=32, learningCoef=2.5) # max 2.5
            assert now.addDay(13).toString() == timeCycle.getNextStep(Level(level=4, levelMax=5)).toString()
            timeCycle = TimeCycle(learningTime=32, learningCoef=1.5) # min 1.5
            assert now.addDay(22).toString() == timeCycle.getNextStep(Level(level=4, levelMax=5)).toString()

            timeCycle = TimeCycle(learningTime=8, learningCoef=2.5) # small time
            assert now.addDay(1).toString() == timeCycle.getNextStep(Level(level=0, levelMax=5)).toString()

            timeCycle = TimeCycle(learningTime=8, learningCoef=2.5) # small time
            assert now.addDay(1).toString() == timeCycle.getNextStep(Level(level=1, levelMax=10)).toString()
