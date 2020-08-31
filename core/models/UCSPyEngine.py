
from pathlib import Path

from core.plotting import make_line_plot
from core.models.Solver import UCSPSolver
from core.models.ScheduleInspector import ScheduleInspector
from core.generators.generate_state import generate_state_from_config
from core.parsers.parse_config import parse_config_file
from core.generators.StateGenerator import StateGenerator
from core.models.ScheduleOperator import ScheduleOperator


class UCSPyEngine:
    """
    UCSPy-Engine

    :param config_file: The JSON file used to configure UCSPy-Engine.  (default: 'ucsp.config.json')
    """

    def __init__(self, config_file="ucsp.config.json"):
        Path("data/logs").mkdir(parents=True, exist_ok=True)
        Path("data/schedules").mkdir(parents=True, exist_ok=True)

        self._config = parse_config_file(config_file)
        self._state = StateGenerator(self._config).generate()

    def solve(self, *args, **kwargs):
        return UCSPSolver(self._config, self._state).solve(*args, **kwargs)

    def plot(self, *args, **kwargs):
        return make_line_plot(*args, **kwargs)

    def inspect(self, *args, **kwargs):
        return ScheduleInspector(
            self._state.fitness_provider,
            ScheduleOperator(self._state.schedule_param)
        ).inspect(*args, **kwargs)
