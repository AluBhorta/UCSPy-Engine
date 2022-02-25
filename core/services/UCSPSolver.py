import os
import datetime

from core.models import Schedule
from core.models.UCSPState import UCSPState
from core.util.bench_time import bench_time


class UCSPSolver:
    """ 
    UCSP Solver

    Solves univesity course scheduling problems using various different algorithms.
    """

    def __init__(self, state: UCSPState):
        self._state = state
        self._logger = state.logger
        self._should_save_schedule = state.should_save_schedule
        self._inspect_final_sch = state.should_inspect_final_schedule
        self.algo = state.algo

    @bench_time
    def solve(self):
        try:
            self.show_args()

            schedule = self.algo.run()

            if self._should_save_schedule:
                self._save_schedule(schedule)
            self._print_final_fitness(schedule)
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

    def _save_schedule(self, schedule: Schedule):
        t = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

        fname = os.path.join(
            os.getcwd(), "data/schedules", f"sch-str-{t}.csv")
        with open(fname, "w") as f:
            f.write(schedule.to_csv())
        self._logger.write(
            f"\nHuman Readable Schedule successfully saved to: {fname}")

        fname = os.path.join(
            os.getcwd(), "data/schedules", f"sch-num-{t}.csv")
        with open(fname, "w") as f:
            f.write(schedule.to_num_csv())
        self._logger.write(
            f"Numeric Schedule successfully saved to: {fname}")

    def _print_final_fitness(self, schedule):
        fit = self._state.fitness_provider.fitness(
            schedule,
            _inspect=self._inspect_final_sch
        )
        self._logger.write("\n-\t-\t-\t-\t-\n")
        self._logger.write(f"Final Fitness: {fit}\n")
