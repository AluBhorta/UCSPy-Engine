import numpy as np
from pandas import read_csv

from data.models import Room, Timeslot, Course, Instructor, CourseGroup, StateManager


def generate_state_from_csv(_dir="data/input_as_csv/iub/autumn19_v0.3/", file_prefix="schedule_params-autumn19 - ") -> StateManager:
    R_DF = read_csv(_dir + file_prefix + "Rooms.csv")
    T_DF = read_csv(_dir + file_prefix + "Timeslots.csv")
    C_DF = read_csv(_dir + file_prefix + "Courses.csv")
    I_DF = read_csv(_dir + file_prefix + "Instructors.csv")
    CG_DF = read_csv(_dir + file_prefix + "CourseGroups.csv")

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
        allowed_courses = ROOMS[i][3]
        if allowed_courses == "ALL_THEORY":
            allowed_courses = all_theory_course_indices
        elif allowed_courses[:4] == "NOT:":
            not_allowed_courses = [int(i)
                                   for i in allowed_courses[4:].split(',')]
            allowed_courses = []
            for c in range(len(COURSES)):
                if c not in not_allowed_courses:
                    allowed_courses.append(c)
        else:
            allowed_courses = [int(i) for i in allowed_courses.split(',')]
        ROOMS[i][3] = allowed_courses

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
