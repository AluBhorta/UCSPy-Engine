from . import ScheduleParam
from .FitnessProvider import FitnessProvider
from .ScheduleGenerator import ScheduleGenerator
from core.logging import UCSPLogger

class UCSPState:
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
