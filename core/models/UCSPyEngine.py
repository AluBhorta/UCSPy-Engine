
from pathlib import Path

from core.plotting import UCSPPlotter
from core.models.Solver import UCSPSolver
from core.models.ScheduleInspector import ScheduleInspector
from core.parsers.parse_config import parse_config_file
from core.generators.StateGenerator import StateGenerator
from core.models.ScheduleOperator import ScheduleOperator


class UCSPyEngine:
    """
    UCSPy-Engine

    :param config_file: The JSON file used to configure UCSPy-Engine. Refer to the configuration documentation (docs/configuration.md) to learn more about it.
    """

    def __init__(self, config_file="ucsp.config.json"):
        Path("data/logs").mkdir(parents=True, exist_ok=True)
        Path("data/schedules").mkdir(parents=True, exist_ok=True)

        self._config = parse_config_file(config_file)
        self._state = StateGenerator(self._config).generate()

    def solve(self, show_args=False, *args, **kwargs):
        """ used to solve a course scheduling problem. 
        
        :param show_args: shows the arguments provided for the current solver when this flag is used.
        """
        solver = UCSPSolver(self._config, self._state, *args, **kwargs)
        if show_args:
            return solver.show_args()
        solver.solve()

    def plot(self, log_file="data/logs/sample.log", *args, **kwargs):
        """ used to plot the performance of the solver i.e. fitness at each epoch. 

        :param log_file: The log file to use for plotting.
        """
        return UCSPPlotter(log_file=log_file, *args, **kwargs).plot()

    def inspect(self, schedule_file="data/schedules/sch-num-sample.csv", *args, **kwargs):
        """ used to inspect the quality of the solution provided, by showing detail constraint violations. 

        :param schedule_file: The numerical schedule file to inspect.
        """
        return ScheduleInspector(
            self._state.fitness_provider,
            ScheduleOperator(self._state.schedule_param)
        ).inspect(schedule_file, *args, **kwargs)
