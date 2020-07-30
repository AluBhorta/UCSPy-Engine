
from core.models.Constraints import HardConstraint, SoftConstraint
from core.constraints import HARD_CONSTRAINT_FUNCS, SOFT_CONSTRAINT_FUNCS


def generate_constraints(constraints_config):

    hc_ids = constraints_config['hard_constraints']['use_ids']
    HARD_CONSTRAINTS = []

    for _id in hc_ids:
        try:
            hc_func = next(f for f in HARD_CONSTRAINT_FUNCS if f['id'] == _id)
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
            sc_func = next(f for f in SOFT_CONSTRAINT_FUNCS if f['id'] == _id)
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
