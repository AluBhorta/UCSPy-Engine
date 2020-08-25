import fire
from pathlib import Path

from core.plotting import make_line_plot
from core.models.Solver import UCSPSolver
from core.util.inspect_schedule import inspect_schedule


class UCSPyEngine:
    """
    UCSPy-Engine

    Solves the univesity course scheduling problems using various intelligent algorithms.
    """

    def __init__(self, config_file="ucsp.config.json"):
        Path("data/logs").mkdir(parents=True, exist_ok=True)
        Path("data/schedules").mkdir(parents=True, exist_ok=True)

        self.solve = UCSPSolver().solve
        self.plot = make_line_plot
        self.inspect = inspect_schedule


if __name__ == "__main__":
    fire.Fire(UCSPyEngine)
    pass
