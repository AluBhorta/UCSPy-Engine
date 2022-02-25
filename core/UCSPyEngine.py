
from core.services.StateGenerator import StateGenerator
from core.services.UCSPSolver import UCSPSolver
from core.services.UCSPPlotter import UCSPPlotter
from core.services.ScheduleInspector import ScheduleInspector


class UCSPyEngine:
    """
    UCSPy-Engine

    :param config_file: The JSON file used to configure UCSPy-Engine. Refer to the configuration documentation (docs/configuration.md) to learn more about it.
    """

    def __init__(self, config_file="ucsp.config.json"):
        self._config_file = config_file

    def solve(self, show_args=False, *args, **kwargs):
        """ used to solve a course scheduling problem. 

        :param show_args: shows the arguments provided for the current solver when this flag is used.
        """
        state = StateGenerator(self._config_file).generate(*args, **kwargs)
        solver = UCSPSolver(state)
        if show_args:
            return solver.show_args()
        solver.solve()

    def plot(self, log_file="data/logs/sample.log", *args, **kwargs):
        """ used to plot the performance of the solver i.e. fitness at each epoch. 

        :param log_file: The log file to use for plotting.
        """
        return UCSPPlotter(log_file=log_file).plot(*args, **kwargs)

    def inspect(self, schedule_file="data/schedules/sch-num-sample.csv", *args, **kwargs):
        """ used to inspect the quality of the solution provided, by showing detail constraint violations. 

        :param schedule_file: The numerical schedule file to inspect.
        """
        state = StateGenerator(self._config_file).generate()
        return ScheduleInspector(state).inspect(schedule_file, *args, **kwargs)
