from ..models.Constraints import HardConstraint, SoftConstraint
from ..models import ScheduleParam

from core.constraints import HARD_CONSTRAINT_FUNCS, SOFT_CONSTRAINT_FUNCS


class ConstraintManager:
    def __init__(
        self,
        constraints_config,
        schedule_param: ScheduleParam
    ):
        self.hard_constraints, self.soft_constraints = self._generate_constraints(
            constraints_config
        )
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

    def _generate_constraints(self, constraints_config):
        hc_ids = constraints_config['hard_constraints']['use_ids']
        HARD_CONSTRAINTS = []

        for _id in hc_ids:
            try:
                hc_func = next(
                    f for f in HARD_CONSTRAINT_FUNCS if f['id'] == _id)
            except StopIteration:
                print(f"ERROR! No such hard constraint found with id = {_id}!")
                exit(-1)

            hc = next(
                c for c in constraints_config['hard_constraints']["constraints"] if c['id'] == _id)

            HARD_CONSTRAINTS.append(
                HardConstraint(
                    hc['id'],
                    hc_func['func'],
                    hc['desc'],
                )
            )

        sc_ids = constraints_config['soft_constraints']['use_ids']
        SOFT_CONSTRAINTS = []

        for _id in sc_ids:
            try:
                sc_func = next(
                    f for f in SOFT_CONSTRAINT_FUNCS if f['id'] == _id)
            except StopIteration:
                print(f"ERROR! No such soft constraint found with id = {_id}!")
                exit(-1)

            sc = next(
                c for c in constraints_config['soft_constraints']["constraints"] if c['id'] == _id)

            SOFT_CONSTRAINTS.append(
                SoftConstraint(
                    sc['id'],
                    sc['unit_penalty'],
                    sc_func['func'],
                    sc['desc'],
                )
            )

        return HARD_CONSTRAINTS, SOFT_CONSTRAINTS
