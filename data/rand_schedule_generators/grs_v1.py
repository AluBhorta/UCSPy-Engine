import numpy as np
from data.data import ROOMS, TIMESLOTS, COURSES, INSTRUCTORS, NUM_OF_ROOMS, NUM_OF_TIMELSOTS, NUM_OF_COURSES, NUM_OF_INSTRUCTORS, NUM_OF_LECS_BEING_OFFERED
from fitness.solution_encoding import decode


def naive_random_schedule():     # generates a random schedule
    # (Room, Timeslot, Course, Instructor)[]
    return np.array([
        (
            np.random.randint(NUM_OF_ROOMS),
            np.random.randint(NUM_OF_TIMELSOTS),
            np.random.randint(NUM_OF_COURSES),
            np.random.randint(NUM_OF_INSTRUCTORS)
        ) for i in np.arange(NUM_OF_LECS_BEING_OFFERED)
    ])


def generate_random_schedule():
    '''Random schedule generator

    satisfies hard constraint 3 & 4 first, when possible
    '''
    Schedule = []

    for Course in COURSES:
        course_idx = Course[0]

        qualified_instructors = []
        for Instructor in INSTRUCTORS:
            if course_idx in Instructor[2]:
                qualified_instructors.append(Instructor[0])

        if not qualified_instructors:
            raise Exception(
                "Error! No qualified instructors for Course %s found!" % Course[1])

        for lec_i in range(Course[2]):
            # TODO (resolving hard constraint 2): before assigning instructor, go thru each qualified_instructors (qi) & check if any lec in S exists at (qi, qi.available_timeslots)
            # if not, take that pair of (qi, qi.available_timeslots)
            instructor_id = np.random.choice(qualified_instructors)
            timeslot_idx = np.random.choice(INSTRUCTORS[instructor_id][3])

            # TODO (resolving hard constraint 1): before assigning room, check if a lecture exists at that (room, timeslot)
            # OR:
            # if len(Course[3]) > 0: use np.random.choice(Course[3])
            # else: np.random.randint(NUM_OF_ROOMS)
            room_idx = np.random.randint(NUM_OF_ROOMS)
            # room_idx = np.random.choice(Course[3])   # optimizes for soft_constraint_1 as well!

            Schedule.append(
                [room_idx, timeslot_idx, course_idx, instructor_id])

    return np.array(Schedule)


def generate_random_schedule_v1():
    '''Random schedule generator V1

    the schedule if generated without Exception will satisfy all the hard constraints
    '''
    S = []

    for Course in COURSES:
        course_idx = Course[0]
        qualified_instructors = _get_qualified_instructors_for(course_idx)

        for lec_i in range(Course[2]):
            instructor_idx, timeslot_idx, room_idx = _get_unique_I_T_R(
                qualified_instructors, course_idx, S)

            S.append(
                [room_idx, timeslot_idx, course_idx, instructor_idx])

    return np.array(S)


def _get_qualified_instructors_for(course_idx):
    qualified_instructors = []
    for Instructor in INSTRUCTORS:
        if course_idx in Instructor[2]:
            qualified_instructors.append(Instructor[0])

    if not qualified_instructors:
        raise Exception(
            "Error! No qualified instructors for course_idx %s found!" % course_idx)

    return qualified_instructors


def _get_unique_I_T_R(qualified_instructors, course_idx, Schedule):
    MAX_RAND_R, MAX_RAND_I_T = 20, 10
    rand_R_counter, rand_I_T_counter = 0, 0

    instructor_idx, timeslot_idx = _get_unique_I_T(
        qualified_instructors, course_idx, Schedule)
    room_idx = np.random.choice(ROOMS[:, 0])

    while True:
        if _R_T_exists(room_idx, timeslot_idx, Schedule):
            if rand_R_counter < MAX_RAND_R:
                timeslot_idx = np.random.choice(ROOMS[:, 0])
                rand_R_counter += 1
                continue
            elif rand_I_T_counter < MAX_RAND_I_T:
                instructor_idx, timeslot_idx = _get_unique_I_T(
                    qualified_instructors, course_idx, Schedule)
                rand_I_T_counter += 1
                continue
            else:
                for instructor_idx in qualified_instructors:
                    for timeslot_idx in TIMESLOTS[:, 0]:
                        if not _I_T_exists(instructor_idx, timeslot_idx, Schedule):
                            for room_idx in ROOMS[:, 0]:
                                if not _R_T_exists(room_idx, timeslot_idx, Schedule):
                                    return (instructor_idx, timeslot_idx, room_idx)

                raise Exception(
                    f"Input Error! No unique (I, T) combination possible for course_idx {course_idx}!")
        else:
            return (instructor_idx, timeslot_idx, room_idx)


def _get_unique_I_T(qualified_instructors, course_idx, Schedule):
    MAX_RAND_T, MAX_RAND_I = 10, 10
    rand_T_counter, rand_I_counter = 0, 0

    instructor_idx = np.random.choice(qualified_instructors)

    # not taking I.available_timeslots into account
    timeslot_idx = np.random.choice(TIMESLOTS[:, 0])
    # timeslot_idx = np.random.choice(INSTRUCTORS[instructor_idx][3])

    while True:
        if _I_T_exists(instructor_idx, timeslot_idx, Schedule):
            if rand_T_counter < MAX_RAND_T:
                timeslot_idx = np.random.choice(TIMESLOTS[:, 0])
                rand_T_counter += 1
                continue
            elif rand_I_counter < MAX_RAND_I:
                instructor_idx = np.random.choice(qualified_instructors)
                rand_I_counter += 1
                continue
            else:
                for instructor_idx in qualified_instructors:
                    for timeslot_idx in TIMESLOTS[:, 0]:
                        if not _I_T_exists(instructor_idx, timeslot_idx, Schedule):
                            return (instructor_idx, timeslot_idx)

                raise Exception(
                    f"Input Error! No unique (I, T) combination possible for course_idx {course_idx}!")
        else:
            return (instructor_idx, timeslot_idx)


def _I_T_exists(I, T, S):
    """ return True if (I, T) exists in S, else false """
    if S:
        S = np.array(S)
        for L in S[:, (3, 1)]:
            if L[0] == I and L[1] == T:
                return True
    return False


def _R_T_exists(R, T, S):
    """ return True if (R, T) exists in S, else false """
    if S:
        S = np.array(S)
        for L in S[:, (0, 1)]:
            if L[0] == R and L[1] == T:
                return True
    return False


# def grs3():
#     S = []

#     for C in COURSES:
#         qualified_instructors = _get_qualified_instructors_for(C.id)

#         for sec in C.sections:
#             instructor, timeslot, room = _get_unique_I_T_R_v3(qualified_instructors, C.id, S)

#             S.append(Class(instructor, timeslot, room, sec))

#     return Schedule(S)
