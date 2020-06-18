"""
# Hard Constraints

if violatesHard:	return 0
else:				return 1 

## Constraints 

1. No two lectures can take place in the same room at the same Timeslot. i.e. unique 2-tuple (R, T)

2. No instructor can take more than one lecture at a given Timeslot. i.e. unique 2-tuple (I, T)

3. Instructors can only take certain courses they are assigned to


Schedule: (Room, Timeslot, Course, Instructor)[]

### How to add a hard constraint

- write a func that takes a Schedule as param
- perform desired violation check on Schedule
- if violates, return True else return False
- add your func to the list HARD_CONSTRAINTS at the end

"""
from data.models import Schedule


def violates_hard_constraint_1(schedule: Schedule):
    """
    Hard Constraint 1: No two lectures can take place in the same room at the same Timeslot
    (R, T)
    """
    # (int room_idx, int[] timeslot_idxs)[]
    unique_room_timeslots = []

    for c in schedule.classes:
        for u_RTs in unique_room_timeslots:
            if c.room.idx == u_RTs[0]:
                c_t_idxs = set(t.idx for t in c.timeslots)
                intersection = list(c_t_idxs.intersection(u_RTs[1]))
                if len(intersection) > 0:
                    return True
        
        unique_room_timeslots.append((c.room.idx, [t.idx for t in c.timeslots]))

    return False


def violates_hard_constraint_2(schedule: Schedule):
    """
    Hard Constraint 2: No instructor can take more than one lecture at a given Timeslot
    (I, T)
    """
    # (int instr_idx, int[] timeslot_idxs)[]
    unique_instr_timeslots = []

    for c in schedule.classes:
        for u_ITs in unique_instr_timeslots:
            if c.instructor.idx == u_ITs[0]:
                c_t_idxs = set(t.idx for t in c.timeslots)
                intersection = list(c_t_idxs.intersection(u_ITs[1]))
                if len(intersection) > 0:
                    return True

        unique_instr_timeslots.append((c.instructor.idx, [t.idx for t in c.timeslots]))

    return False


# def violates_hard_constraint_3(schedule: Schedule):
#     """
#     Hard Constraint 3: Instructors can only take certain courses they are assigned to
#     """
#     for lec in schedule:
#         course_idx = lec[2]

#         decoded_lec = decode(lec)
#         qualified_courses = decoded_lec[3][2]

#         if course_idx not in qualified_courses:
#             return True

#     return False



"""
Contains all the hard-constraint-funcs
"""
HARD_CONSTRAINTS = [
    violates_hard_constraint_1,
    violates_hard_constraint_2,
    # violates_hard_constraint_3,
]
