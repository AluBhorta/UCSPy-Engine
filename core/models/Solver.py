import os
import json
import datetime
from time import perf_counter

from core.models import Schedule, StateManager
from core.logging import UCSPLogger
from algorithms import ALL_ALGORITHMS


class UCSPSolver:
    """ 
    UCSP Solver

    Solves the univesity course scheduling problems using various intelligent algorithms.
    """

    def __init__(self, config, state: StateManager):
        self._config = config
        self._state = state
        self._logger = UCSPLogger(config['save_logs'])

        self._save_sch = config['save_schedule']
        self._inspect_final_sch = config['inspect_final_schedule']
        self._min_acceptable_fitness = config["fitness"]['min_acceptable_fitness']

        self._algo_name = config['algorithm']['use']

    def solve(self, algo_name=None, *args, **kwargs):
        _algo = self._get_algo(algo_name)
        self._logger.write(f"Running: {_algo.__name__}...\n")

        t1 = perf_counter()
        sch = _algo(self._logger, self._state).run(*args, **kwargs)
        t2 = perf_counter()

        self._write_schedule(sch)
        self._logger.write(f"\nTime taken: {t2-t1} s")

    def _get_algo(self, algo_name=None):
        name = algo_name or self._algo_name
        algo = ALL_ALGORITHMS.get(name)
        if not hasattr(algo, 'run'):
            raise Exception(f"ERROR! Invalid algo name provided: {name}")
        return algo

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

        fit = self._state.fitness(sch, _inspect=self._inspect_final_sch)
        print(f"Final fitness: {fit}")
