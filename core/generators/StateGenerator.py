
import json
from algorithms import ALL_ALGORITHMS
from core.models.Algorithm import Algorithm

from core.models.UCSPState import UCSPState
from core.models.ConstraintManager import ConstraintManager
from core.services.FitnessProvider import FitnessProvider
from core.generators.schedule.DefaultScheduleGenerator import DefaultScheduleGenerator
from core.generators.generate_constraints import generate_constraints
from core.util.parse_schedule_params import parse_schedule_params
from core.fitness import FITNESS_PROVIDERS
from core.fitness.TanhFitnessProvider import TanhFitnessProvider
from core.services.UCSPLogger import UCSPLogger


class StateGenerator:
    def __init__(self, config_file):
        self.config = self._parse_config_file(config_file)

    def generate(self) -> UCSPState:
        self.schedule_param = parse_schedule_params(
            self.config['schedule_param'])

        HARD_CONSTRAINTS, SOFT_CONSTRAINTS = generate_constraints(
            self.config['constraints']
        )
        constraint_manager = ConstraintManager(
            HARD_CONSTRAINTS, SOFT_CONSTRAINTS, self.schedule_param
        )
        self.fitness_provider = self._get_fitness_provider(constraint_manager)

        self.schedule_generator = DefaultScheduleGenerator(self.schedule_param)

        self.logger = UCSPLogger(self.config['save_logs'])

        if self.config["fitness"].get('min_acceptable_fitness'):
            self._min_acceptable_fitness = self.config["fitness"]['min_acceptable_fitness']
        else:
            self._min_acceptable_fitness = 0 if self.fitness_provider.is_reverse() else 1

        self.algo_name = self.config['algorithm']['use']

        return UCSPState(
            self.schedule_param,
            self.fitness_provider,
            self.schedule_generator,
            self.logger,
            should_save_schedule=self.config['save_schedule'],
            should_inspect_final_schedule=self.config['inspect_final_schedule'],
            get_algo=self._get_algo
        )

    def _parse_config_file(self, fpath="ucsp.config.json"):
        with open(fpath) as f:
            return json.load(f)

    def _get_fitness_provider(self, constraint_manager: ConstraintManager) -> FitnessProvider:
        fit_func_name = self.config['fitness']['use']
        fp = FITNESS_PROVIDERS.get(fit_func_name, TanhFitnessProvider)

        if not hasattr(fp, 'fitness'):
            raise Exception(f"ERROR! Invalid fitness provided: {fp}")
        return fp(constraint_manager)

    def _get_algo(self, *args, **kwargs) -> Algorithm:
        algo = ALL_ALGORITHMS.get(self.algo_name)

        if not hasattr(algo, 'run'):
            raise Exception(f"ERROR! Invalid algo name provided: {algo}")

        return algo(
            self.schedule_param,
            self.fitness_provider,
            self.schedule_generator,
            self.logger,
            min_acceptable_fitness=self._min_acceptable_fitness,
            *args, **kwargs
        )
