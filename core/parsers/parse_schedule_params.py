import numpy as np
from pandas import read_csv
import os

from core.models import Room, Timeslot, Course, Instructor, CourseGroup, StateManager


def generate_state_from_csv(_dir="data/schedule_params/default") -> StateManager:
    r_fname = "rooms.csv"
    t_fname = "timeslots.csv"
    c_fname = "courses.csv"
    i_fname = "instructors.csv"
    cg_fname = "course_groups.csv"
    try:
        R_DF = read_csv(os.path.join(os.getcwd(), _dir, r_fname))
        T_DF = read_csv(os.path.join(os.getcwd(), _dir, t_fname))
        C_DF = read_csv(os.path.join(os.getcwd(), _dir, c_fname))
        I_DF = read_csv(os.path.join(os.getcwd(), _dir, i_fname))
        CG_DF = read_csv(os.path.join(os.getcwd(), _dir, cg_fname))
    except:
        raise Exception(
            f"ERROR! Required files not found in {_dir}. They should be named as follows: {r_fname, t_fname, c_fname, i_fname, cg_fname}"
        )

    ROOMS = R_DF.to_numpy()
    TIMESLOTS = T_DF.to_numpy()
    COURSES = C_DF.to_numpy()
    INSTRUCTORS = I_DF.to_numpy()
    COURSE_GROUPS = CG_DF.to_numpy()

    all_theory_courses = list(filter(lambda x: x[5] == "Theory", COURSES))
    all_theory_course_indices = [c[0] for c in all_theory_courses]

    """ parse collections """

    # Rooms - col 3: allowed_courses
    for i in range(len(ROOMS)):
        allowed_course_idxs = ROOMS[i][3]
        if allowed_course_idxs == "ALL_THEORY":
            allowed_course_idxs = all_theory_course_indices
        elif allowed_course_idxs[:4] == "NOT:":
            not_allowed_courses = [int(i)
                                   for i in allowed_course_idxs[4:].split(',')]
            allowed_course_idxs = []
            for c in range(len(COURSES)):
                if c not in not_allowed_courses:
                    allowed_course_idxs.append(c)
        else:
            allowed_course_idxs = [int(i)
                                   for i in allowed_course_idxs.split(',')]
        ROOMS[i][3] = allowed_course_idxs

    # Instructors - col 2, 3
    for i in range(len(INSTRUCTORS)):
        INSTRUCTORS[i][2] = str_to_array(INSTRUCTORS[i][2])
        INSTRUCTORS[i][3] = str_to_array(INSTRUCTORS[i][3])

    # CourseGroups - col 2, 3
    for i in range(len(COURSE_GROUPS)):
        COURSE_GROUPS[i][2] = str_to_array(COURSE_GROUPS[i][2])
        COURSE_GROUPS[i][3] = str_to_array(COURSE_GROUPS[i][3])

    # print_params(ROOMS, TIMESLOTS, COURSES, INSTRUCTORS, COURSE_GROUPS)

    '''
    TODO: deduce implied sanity check
    if NUM_OF_LECS_BEING_OFFERED > MAX_LECS_THAT_CAN_BE_OFFERED:
    '''

    Rooms = [Room(r[0], r[1], r[2], r[3]) for r in ROOMS]
    Timeslots = [Timeslot(t[0], t[1], t[2]) for t in TIMESLOTS]
    Courses = [Course(c[0], c[1], c[2], c[3], c[4], c[5]) for c in COURSES]
    Instructors = [Instructor(i[0], i[1], i[2], i[3]) for i in INSTRUCTORS]
    CourseGroups = [CourseGroup(cg[0], cg[1], cg[2], cg[3])
                    for cg in COURSE_GROUPS]

    # print_params(Rooms, Timeslots, Courses, Instructors, CourseGroups)

    # TODO: do a sanity check that the arrays are not empty and contain the objects contain the right attributes
    return StateManager(
        Rooms, Timeslots, Courses, Instructors, CourseGroups)


def str_to_array(str_values):
    values = []
    for i in str_values.split(","):
        if i is not '':
            values.append(int(i))
    return np.array(values)


def print_params(ROOMS, TIMESLOTS, COURSES, INSTRUCTORS, COURSE_GROUPS):
    print('\nROOMS:')
    print(ROOMS)
    print('\nTIMESLOTS:')
    print(TIMESLOTS)
    print('\nCOURSES:')
    print(COURSES)
    print('\nINSTRUCTORS:')
    print(INSTRUCTORS)
    print('\nCOURSE_GROUPS:')
    print(COURSE_GROUPS)
    print('\n')
