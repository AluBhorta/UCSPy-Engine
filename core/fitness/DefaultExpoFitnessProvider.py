from math import exp

from core.models.FitnessProvider import FitnessProvider
from core.services.ConstraintManager import ConstraintManager


class DefaultExpoFitnessProvider(FitnessProvider):
    """ 
    DefaultExpoFitnessProvider
    
    fitness of 1 is perfect & 0 is infeasible
    """

    def __init__(self, constraint_manager: ConstraintManager):
        super(DefaultExpoFitnessProvider, self).__init__(constraint_manager)

    def compare(self, fitness1, fitness2):
        return True if fitness1 > fitness2 else False

    def fitness(self, schedule, _inspect=False, **kwargs):
        violates_a_hc = self.constraint_manager.violates_a_hard_constraint(
            schedule, _inspect)
        hpm = 0 if violates_a_hc else 1

        tsp = self.constraint_manager.total_soft_penalty(schedule, _inspect)
        if tsp < 0:
            raise Exception(f"Error! Total soft penalty cannot be negative!")

        return hpm / (1 + exp(tsp))
