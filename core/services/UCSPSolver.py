import os
import json
import datetime

from core.models import Schedule
from core.logging import UCSPLogger
from algorithms import ALL_ALGORITHMS
from core.models.Algorithm import Algorithm
from core.models.UCSPState import UCSPState
from core.util import bench_time, pretty_print_results


class UCSPSolver:
    """ 
    UCSP Solver

    Solves univesity course scheduling problems using various different algorithms.
    """

    def __init__(self, config, state: UCSPState, *args, **kwargs):
        self._state = state
        self._logger = state.logger

        self._save_sch = config['save_schedule']
        self._inspect_final_sch = config['inspect_final_schedule']
        self._algo_name = config['algorithm']['use']

        if config["fitness"].get('min_acceptable_fitness'):
            self._min_acceptable_fitness = config["fitness"]['min_acceptable_fitness']
        else:
            self._min_acceptable_fitness = 0 if self._state.fitness_provider.is_reverse() else 1

        self.algo = self._get_algo(
            min_acceptable_fitness=self._min_acceptable_fitness,
            *args, **kwargs
        )

    @bench_time
    def solve(self):
        try:
            self.show_args()
            
            schedule = self.algo.run()
            self._write_schedule(schedule)
            return
        except KeyboardInterrupt:
            print("Stopped...")

    def show_args(self):
        self._logger.write(
            f"Fitness provider: {self._state.fitness_provider.__class__.__name__}")
        self._logger.write(f"Algo: {type(self.algo).__name__}")
        default_args = self.algo.get_default_args()
        self._logger.write(
            f"Arguments used for - {type(self.algo).__name__}: {default_args}\n")

    def _get_algo(self, *args, **kwargs) -> Algorithm:
        name = self._algo_name
        algo = ALL_ALGORITHMS.get(name)

        if not hasattr(algo, 'run'):
            raise Exception(f"ERROR! Invalid algo name provided: {name}")

        return algo(
            self._state.schedule_param,
            self._state.fitness_provider,
            self._state.schedule_generator,
            self._logger,
            *args, **kwargs
        )

    def _write_schedule(self, sch: Schedule):
        if self._save_sch:
            t = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

            fname = os.path.join(
                os.getcwd(), "data/schedules", f"sch-str-{t}.csv")
            with open(fname, "w") as f:
                f.write(sch.to_csv())
            self._logger.write(
                f"\nHuman Readable Schedule successfully saved to: {fname}")

            fname = os.path.join(
                os.getcwd(), "data/schedules", f"sch-num-{t}.csv")
            with open(fname, "w") as f:
                f.write(sch.to_num_csv())
            self._logger.write(
                f"Numeric Schedule successfully saved to: {fname}")

        fit = self._state.fitness_provider.fitness(
            sch, _inspect=self._inspect_final_sch
        )
        pretty_print_results(fitness_value=fit)
