from . import ScheduleParam
from ..services.FitnessProvider import FitnessProvider
from .ScheduleGenerator import ScheduleGenerator
from core.services.UCSPLogger import UCSPLogger


class UCSPState:
    def __init__(
        self,
        schedule_param: ScheduleParam,
        fitness_provider: FitnessProvider,
        schedule_generator: ScheduleGenerator,
        logger: UCSPLogger,
        should_save_schedule,
        should_inspect_final_schedule,
        get_algo
    ):
        self.schedule_param = schedule_param
        self.fitness_provider = fitness_provider
        self.schedule_generator = schedule_generator
        self.logger = logger
        self.should_save_schedule = should_save_schedule
        self.should_inspect_final_schedule = should_inspect_final_schedule
        self.get_algo = get_algo
