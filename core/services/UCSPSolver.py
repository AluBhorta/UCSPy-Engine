import os
import json
import datetime

from core.models import Schedule
from core.services.UCSPLogger import UCSPLogger
from algorithms import ALL_ALGORITHMS
from core.models.Algorithm import Algorithm
from core.models.UCSPState import UCSPState
from core.util import bench_time, pretty_print_results


class UCSPSolver:
    """ 
    UCSP Solver

    Solves univesity course scheduling problems using various different algorithms.
    """

    def __init__(self, state: UCSPState, *args, **kwargs):
        self._state = state
        self._logger = state.logger
        self._save_sch = state.should_save_schedule
        self._inspect_final_sch = state.should_inspect_final_schedule
        self.algo = state.get_algo(*args, **kwargs)

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
            f"Fitness provider: {self._state.fitness_provider.__class__.__name__}"
        )
        self._logger.write(f"Algo: {type(self.algo).__name__}")
        default_args = self.algo.get_default_args()
        self._logger.write(
            f"Arguments used for - {type(self.algo).__name__}: {default_args}\n"
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
