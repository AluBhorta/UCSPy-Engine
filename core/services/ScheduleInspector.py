
from pandas import read_csv
import os
from core.models.UCSPState import UCSPState

from core.services.ScheduleOperator import ScheduleOperator
from core.models.FitnessProvider import FitnessProvider


class ScheduleInspector:
    """ Schedule Inspector 

        Inspect the quality of a schedule.
    """

    def __init__(self, state: UCSPState):
        self.fitness_provider = state.fitness_provider
        self.schedule_operator = ScheduleOperator(state.schedule_param)

    def inspect(self, schedule_file):
        numrepr = self._parse_numrepr_from_file(schedule_file)
        sch = self.schedule_operator.numrepr_to_sch(numrepr)

        tsp = self.fitness_provider.constraint_manager.total_soft_penalty(sch)
        f_val = self.fitness_provider.fitness(sch, _inspect=True)

        self.pretty_print_results(tsp, f_val, self.fitness_provider)

    def _parse_numrepr_from_file(self, schedule_file):
        return read_csv(
            os.path.join(os.getcwd(), schedule_file)
        ).to_numpy()

    def pretty_print_results(self, tsp=None, fitness_value=None, fitness_provider=None):
        print("\n-\t-\t-\t-\t-\n")
        fitness_provider and print(
            f"Fitness provider: {fitness_provider.__class__.__name__}")
        fitness_value and print(f"Final Fitness: {fitness_value}")
        tsp and print(f"Total Soft Penalty: {tsp}")
