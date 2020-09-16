import os
import json
import datetime
from time import perf_counter

from core.models import Schedule
from core.logging import UCSPLogger
from algorithms import ALL_ALGORITHMS
from core.models.Algorithm import Algorithm
from core.models.UCSPState import UCSPState


class UCSPSolver:
    """ 
    UCSP Solver

    Solves the univesity course scheduling problem using various intelligent algorithms.
    """

    def __init__(self, config, state: UCSPState):
        self._state = state
        self._logger = state.logger

        self._save_sch = config['save_schedule']
        self._inspect_final_sch = config['inspect_final_schedule']
        self._min_acceptable_fitness = config["fitness"]['min_acceptable_fitness']
        self._algo_name = config['algorithm']['use']

    def solve(self, algo_name=None, *args, **kwargs):
        algo = self._get_algo(algo_name, *args, **kwargs)
        self._logger.write(f"Running: {type(algo).__name__}...")
        default_args = algo.get_default_args()
        self._logger.write(f"Default arguments: {default_args}\n")

        t1 = perf_counter()
        sch = algo.run()
        t2 = perf_counter()

        self._write_schedule(sch)
        self._logger.write(f"\nTime taken: {t2-t1} s")

        return sch

    def stop(self):
        raise NotImplementedError

    def _get_algo(self, algo_name=None, *args, **kwargs) -> Algorithm:
        name = algo_name or self._algo_name
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
                f"\nHuman Readable Schedule successfully saved to {fname}")

            fname = os.path.join(
                os.getcwd(), "data/schedules", f"sch-num-{t}.csv")
            with open(fname, "w") as f:
                f.write(sch.to_num_csv())
            self._logger.write(
                f"\nNumeric Schedule successfully saved to {fname}")
        else:
            print("\nFinal Schedule: \n")
            print(sch.to_tsv())

        fit = self._state.fitness_provider.fitness(
            sch, _inspect=self._inspect_final_sch
        )
        print(f"Final fitness: {fit}")
