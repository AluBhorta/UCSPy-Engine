from abc import ABC, abstractmethod

from core.logging import UCSPLogger
from core.models.FitnessProvider import FitnessProvider
from core.models import ScheduleParam
from core.models.ScheduleGenerator import ScheduleGenerator


class Algorithm(ABC):
    def __init__(
        self,
        schedule_param: ScheduleParam,
        fitness_provider: FitnessProvider,
        schedule_generator: ScheduleGenerator,
        logger: UCSPLogger
    ):
        self.schedule_param = schedule_param
        self.fitness_provider = fitness_provider
        self.schedule_generator = schedule_generator
        self.logger = logger

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_default_args(self, *args, **kwargs):
        """ return the default arguments of the algorithm as a dictionary. """
        raise NotImplementedError
