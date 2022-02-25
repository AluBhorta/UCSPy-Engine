
import json
from core.algorithms import ALL_ALGORITHMS
from core.models.Algorithm import Algorithm

from core.models.UCSPState import UCSPState
from core.services.ConstraintManager import ConstraintManager
from core.models.FitnessProvider import FitnessProvider
from core.services.DefaultScheduleGenerator import DefaultScheduleGenerator
from core.util.parse_schedule_params import parse_schedule_params
from core.fitness import FITNESS_PROVIDERS
from core.fitness.TanhFitnessProvider import TanhFitnessProvider
from core.services.UCSPLogger import UCSPLogger


class StateGenerator:
    def __init__(self, config_file):
        self.config = self._parse_config_file(config_file)

    def generate(self, *args, **kwargs) -> UCSPState:
        self.schedule_param = parse_schedule_params(
            self.config['schedule_param'])

        constraint_manager = ConstraintManager(
            constraints_config=self.config['constraints'],
            schedule_param=self.schedule_param
        )
        self.fitness_provider = self._get_fitness_provider(constraint_manager)

        self.schedule_generator = DefaultScheduleGenerator(self.schedule_param)

        self.logger = UCSPLogger(self.config['save_logs'])

        if self.config["fitness"].get('min_acceptable_fitness'):
            self._min_acceptable_fitness = self.config["fitness"]['min_acceptable_fitness']
        else:
            self._min_acceptable_fitness = 0 if self.fitness_provider.is_reverse() else 1

        algo_name = self.config['algorithm']['use']
        algo = self._get_algo(algo_name, *args, **kwargs)

        return UCSPState(
            self.schedule_param,
            self.fitness_provider,
            self.schedule_generator,
            self.logger,
            algo,
            should_save_schedule=self.config['save_schedule'],
            should_inspect_final_schedule=self.config['inspect_final_schedule'],
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

    def _get_algo(self, algo_name, *args, **kwargs) -> Algorithm:
        algo = ALL_ALGORITHMS.get(algo_name)

        if not hasattr(algo, 'run'):
            raise Exception(f"ERROR! Invalid algo name provided: {algo_name}")

        return algo(
            self.schedule_param,
            self.fitness_provider,
            self.schedule_generator,
            self.logger,
            min_acceptable_fitness=self._min_acceptable_fitness,
            *args, **kwargs
        )
