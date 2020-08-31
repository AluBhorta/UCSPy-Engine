
from core.models.UCSPState import UCSPState
from core.models.ConstraintManager import ConstraintManager
from core.models.FitnessProvider import FitnessProvider
from core.generators.schedule.DefaultScheduleGenerator import DefaultScheduleGenerator
from core.generators.generate_constraints import generate_constraints
from core.parsers.parse_schedule_params import parse_schedule_params
from core.fitness import FITNESS_PROVIDERS
from core.fitness.TanhFitnessProvider import TanhFitnessProvider
from core.logging import UCSPLogger


class StateGenerator:
    def __init__(self, config):
        self.schedule_param_config = config['schedule_param']
        self.constraints_config = config['constraints']
        self.fit_func_name = config['fitness']['use']
        self.save_logs = config['save_logs']

    def generate(self) -> UCSPState:
        schedule_param = parse_schedule_params(self.schedule_param_config)

        HARD_CONSTRAINTS, SOFT_CONSTRAINTS = generate_constraints(
            self.constraints_config
        )
        constraint_manager = ConstraintManager(
            HARD_CONSTRAINTS, SOFT_CONSTRAINTS, schedule_param
        )
        fitness_provider = self._get_fitness_provider(constraint_manager)

        schedule_generator = DefaultScheduleGenerator(schedule_param)

        logger = UCSPLogger(self.save_logs)

        return UCSPState(schedule_param, fitness_provider, schedule_generator, logger)

    def _get_fitness_provider(self, constraint_manager: ConstraintManager) -> FitnessProvider:
        fp = FITNESS_PROVIDERS.get(self.fit_func_name, TanhFitnessProvider)

        if not hasattr(fp, 'fitness'):
            raise Exception(f"ERROR! Invalid fitness provided: {fp}")
        return fp(constraint_manager)
