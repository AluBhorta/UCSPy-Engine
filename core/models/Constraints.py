
# from core.models import Schedule


class HardConstraint:
    def __init__(self, _id, violates_func, desc):
        self._id = _id
        self._violates_func = violates_func
        self.desc = desc

    def violates(self, sch) -> bool:
        # def violates(self, sch: Schedule) -> bool:
        return self._violates_func(sch)


class SoftConstraint:
    def __init__(self, _id, unit_penalty, penalty_func, desc):
        self._id = _id
        self._unit_penalty = unit_penalty
        self._penalty_func = penalty_func
        self.desc = desc

    def penalty_of(self, sch, state, _inspect=False) -> float:
        return self._penalty_func(sch, state, self._unit_penalty, _inspect)
