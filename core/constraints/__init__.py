
from core.constraints.hard.hard_constraint_1 import violates_hard_constraint_1
from core.constraints.hard.hard_constraint_2 import violates_hard_constraint_2

from core.constraints.soft.soft_constraint_1 import penalty_of_soft_constraint_1
from core.constraints.soft.soft_constraint_2 import penalty_of_soft_constraint_2
from core.constraints.soft.soft_constraint_3 import penalty_of_soft_constraint_3
from core.constraints.soft.soft_constraint_4 import penalty_of_soft_constraint_4
from core.constraints.soft.soft_constraint_5 import penalty_of_soft_constraint_5
from core.constraints.soft.soft_constraint_6 import penalty_of_soft_constraint_6
from core.constraints.soft.soft_constraint_7 import penalty_of_soft_constraint_7
from core.constraints.soft.soft_constraint_8 import penalty_of_soft_constraint_8


HARD_CONSTRAINT_FUNCS = [
    {
        "id": 1, "func": violates_hard_constraint_1,
        "desc": "No two classes can take place in the same room at the same Timeslot."
    },
    {
        "id": 2, "func": violates_hard_constraint_2,
        "desc": "No Instructor can take more than one class at a given Timeslot."
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
        "id": 5, "unit_penalty": 1.0, "func": penalty_of_soft_constraint_5,
        "desc": "If a Course has 2 Lectures Per Week, it should take place in a composite Timeslot i.e. with Day code of 'ST' or 'MW'."
    },
    {
        "id": 6, "unit_penalty": 0.8, "func": penalty_of_soft_constraint_6,
        "desc": "The Lab Section of a Course (if any) should be placed in a Timeslot that is before or after the corresponding Theory Section."
    },
    {
        "id": 7, "unit_penalty": 0.6, "func": penalty_of_soft_constraint_7,
        "desc": "The Theory Section and the corresponding Lab Section of a Course (if any) should be taken by the same Instructor."
    },
    {
        "id": 8, "unit_penalty": 0.9, "func": penalty_of_soft_constraint_8,
        "desc": "Instructors have minimum credit load requirements."
    },
]
