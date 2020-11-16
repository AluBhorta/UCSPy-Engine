
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

    :param config_file: The JSON file used to configure UCSPy-Engine.  (default: 'ucsp.config.json')
    \n
    :param config: A config dict object used to configure UCSPy-Engine as an alternative to the config_file.  (default: None)
    \n
    """

    def __init__(self, config_file="ucsp.config.json", config=None):
        Path("data/logs").mkdir(parents=True, exist_ok=True)
        Path("data/schedules").mkdir(parents=True, exist_ok=True)

        self._solvers = []
        self._config = config if config \
            else parse_config_file(config_file)

    def solve(self, *args, **kwargs):
        config = kwargs.get('config', self._config)
        solver = UCSPSolver(config)
        self._solvers.append(solver)
        return solver.solve(*args, **kwargs)

    def plot(self, *args, **kwargs):
        return UCSPPlotter(*args, **kwargs).plot()

    def inspect(self, *args, **kwargs):
        config = kwargs.get('config', self._config)
        state = StateGenerator(config).generate()

        return ScheduleInspector(
            state.fitness_provider,
            ScheduleOperator(state.schedule_param)
        ).inspect(*args, **kwargs)
