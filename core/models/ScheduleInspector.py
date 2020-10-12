
from pandas import read_csv
import os

from core.util import _str_to_array
from core.models.ScheduleOperator import ScheduleOperator
from core.models.FitnessProvider import FitnessProvider


class ScheduleInspector:
    """ Schedule Inspector 

        Inspect the quality of a schedule.
    """

    def __init__(self, fitness_provider: FitnessProvider, schedule_operator: ScheduleOperator):
        self.fitness_provider = fitness_provider
        self.schedule_operator = schedule_operator

    def inspect(self, schedule_file):
        numrepr = self._parse_numrepr_from_file(schedule_file)
        sch = self.schedule_operator.numrepr_to_sch(numrepr)

        tsp = self.fitness_provider.constraint_manager.total_soft_penalty(sch)
        f_val = self.fitness_provider.fitness(sch, _inspect=True)

        print("\n-\t-\t-\t-\t-\n")
        print(f"Total Soft Penalty: {tsp}")
        print(f"Final Fitness: {f_val}")
        print(f"Fitness provider: {self.fitness_provider.__class__.__name__}")

    def _parse_numrepr_from_file(self, schedule_file):
        return read_csv(
            os.path.join(os.getcwd(), schedule_file)
        ).to_numpy()
