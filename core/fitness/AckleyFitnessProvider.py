
import math

from core.services.FitnessProvider import FitnessProvider
from core.models.ConstraintManager import ConstraintManager


class AckleyFitnessProvider(FitnessProvider):
    """ 
    AckleyFitnessProvider (experimental)

    fitness of 0 is perfect & infinity is infeasible
    """
    def __init__(self, constraint_manager: ConstraintManager):
        super(AckleyFitnessProvider, self).__init__(constraint_manager)

    def compare(self, fitness1, fitness2):
        return True if fitness1 < fitness2 else False

    def fitness(self, schedule, _inspect=False, **kwargs):
        violates_a_hc = self.constraint_manager.violates_a_hard_constraint(
            schedule, _inspect)
        if violates_a_hc:
            return math.inf

        tsp = self.constraint_manager.total_soft_penalty(schedule, _inspect)
        if tsp < 0:
            raise Exception(f"Error! Total soft penalty cannot be negative!")

        return self._ackley(tsp)

    def _ackley(self, tsp, a=1.0, b=0.01, c=2*math.pi):
        first_sum = tsp**2.0
        second_sum = math.cos(c*tsp)

        return -a*math.exp(-b*math.sqrt(first_sum)) - math.exp(second_sum) + a + math.e
