import fire
from pathlib import Path

from core.plotting import make_line_plot
from core.models.Solver import UCSPSolver
from core.models.Inspector import Inspector
from core.generators.generate_state import generate_state_from_config
from core.parsers.parse_config import parse_config_file


class UCSPyEngine:
    """
    UCSPy-Engine

    :param config_file: The JSON file used to configure UCSPy-Engine.  (default: 'ucsp.config.json')
    """

    def __init__(self, config_file="ucsp.config.json"):
        Path("data/logs").mkdir(parents=True, exist_ok=True)
        Path("data/schedules").mkdir(parents=True, exist_ok=True)

        self._config = parse_config_file(config_file)
        self._state = generate_state_from_config(self._config)

        # main services: TODO - convert to methods
        self.solve = UCSPSolver(self._config, self._state).solve
        self.plot = make_line_plot
        self.inspect = Inspector(self._state).inspect


if __name__ == "__main__":
    fire.Fire(UCSPyEngine)
