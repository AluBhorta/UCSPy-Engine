import fire
from pathlib import Path

from core.plotting import make_line_plot
from core.models.Solver import UCSPSolver


class UCSPyEngine:
    """
    UCSPy-Engine

    Solves univesity course scheduling problems using various intelligent algorithms.
    """

    def __init__(self):
        Path("data/logs").mkdir(parents=True, exist_ok=True)
        Path("data/schedules").mkdir(parents=True, exist_ok=True)
        self.solver = UCSPSolver
        self.plot = make_line_plot


if __name__ == "__main__":
    fire.Fire(UCSPyEngine)
    pass
