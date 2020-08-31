import numpy as np

from core.models.FitnessProvider import FitnessProvider
from core.models.ConstraintManager import ConstraintManager


class TanhFitnessProvider(FitnessProvider):
    def __init__(self, constraint_manager: ConstraintManager, relax_coeff=0.01):
        super(TanhFitnessProvider, self).__init__(constraint_manager)
        self.relax_coeff = relax_coeff

    def fitness(self, schedule, _inspect=False, **kwargs):
        violates_a_hc = self.constraint_manager.violates_a_hard_constraint(
            schedule, _inspect)
        if violates_a_hc:
            return 1

        tsp = self.constraint_manager.total_soft_penalty(schedule, _inspect)
        if tsp < 0:
            raise Exception(f"Error! Total soft penalty cannot be negative!")
        return np.tanh(self.relax_coeff * tsp)

    def flat_fitness(self, flat_schedule, **kwargs):
        # NOTE: needs `ScheduleOperator`
        # sch = so.deflatten(sch)
        # return self.fitness(sch)
        pass

    def numrepr_fitness(self, numrepr_schedule, **kwargs):
        pass
