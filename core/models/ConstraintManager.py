from typing import List
from .Constraints import HardConstraint, SoftConstraint
from . import ScheduleParam, Schedule


class ConstraintManager:
    def __init__(self, HARD_CONSTRAINTS: List[HardConstraint], SOFT_CONSTRAINTS: List[SoftConstraint], schedule_param: ScheduleParam):
        self.hard_constraints = HARD_CONSTRAINTS
        self.soft_constraints = SOFT_CONSTRAINTS
        self.schedule_param = schedule_param

    def violates_a_hard_constraint(self, schedule, _inspect=False) -> bool:
        for hard_constraint in self.hard_constraints:
            if hard_constraint.violates(schedule):
                if _inspect:
                    print(
                        f"# Hard Constraint {hard_constraint._id} Violation ('{hard_constraint.desc}' !")
                return True
        return False

    def total_soft_penalty(self, schedule, _inspect=False) -> float:
        total_penalty = 0

        for soft_constraint in self.soft_constraints:
            total_penalty += soft_constraint.penalty_of(
                schedule, self.schedule_param, _inspect=_inspect
            )

        return total_penalty
