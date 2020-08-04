
from core.constraints.hard.hard_constraint_1 import violates_hard_constraint_1
from core.constraints.hard.hard_constraint_2 import violates_hard_constraint_2

from core.constraints.soft.soft_constraint_1 import penalty_of_soft_constraint_1
from core.constraints.soft.soft_constraint_2 import penalty_of_soft_constraint_2
from core.constraints.soft.soft_constraint_3 import penalty_of_soft_constraint_3
from core.constraints.soft.soft_constraint_4 import penalty_of_soft_constraint_4
from core.constraints.soft.soft_constraint_5 import penalty_of_soft_constraint_5


""" to learn how to add new constraints, read `core/constraints/modify_constraints.md` """

HARD_CONSTRAINT_FUNCS = [
    {
        "id": 1, "func": violates_hard_constraint_1,
        "desc": "No two lectures can take place in the same room at the same Timeslot"
    },
    {
        "id": 2, "func": violates_hard_constraint_2,
        "desc": "No instructor can take more than one lecture at a given Timeslot"
    },
]

SOFT_CONSTRAINT_FUNCS = [
    {
        "id": 1, "unit_penalty": 0.9, "func": penalty_of_soft_constraint_1,
        "desc": "Instructors should only take certain courses they are are assigned to."
    },
    {
        "id": 2, "unit_penalty": 0.85, "func": penalty_of_soft_constraint_2,
        "desc": "A particular Room should only allow Classes of certain Courses."
    },
    {
        "id": 3, "unit_penalty": 0.6, "func": penalty_of_soft_constraint_3,
        "desc": "CourseGroups have Timeslot preferences."
    },
    {
        "id": 4, "unit_penalty": 0.5, "func": penalty_of_soft_constraint_4,
        "desc": "Instructors have Timeslot preferences."
    },
    {
        "id": 5, "unit_penalty": 0.8, "func": penalty_of_soft_constraint_5,
        "desc": "Lectures of the same Class (of a Course) should be taken at one day intervals, if the Course has more than one Lectures per week."
    },
]
