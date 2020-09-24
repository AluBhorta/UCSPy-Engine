
from abc import ABC, abstractmethod
from . import ScheduleParam, Schedule

class ScheduleGenerator(ABC):
    def __init__(self, schedule_param: ScheduleParam):
        self.schedule_param = schedule_param

    @abstractmethod
    def generate(self, *args, **kwargs) -> Schedule:
        raise NotImplementedError
