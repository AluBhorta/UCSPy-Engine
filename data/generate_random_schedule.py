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


def generate_random_schedule2():
    '''Random schedule generator 2
    the schedule generated MUST satisfy all the hard constraints
    '''
    S = []

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
            instructor_idx, timeslot_idx, room_idx = None, None, None

            for qi in qualified_instructors:
                for ats in qi[3]:    # available_timeslot in I.available_timeslots
                    # is (I, T) unique in S i.e. unique (qi[0], ats)
                    if is_unique_I_T(qi[0], ats, S):
                        #   yes: pick a Room (?allowed for the course) that is avialable at T i.e. unique (R, ats)
                        r = get_free_room_at(ats, S)
                        if r:
                            room_idx = r
                            timeslot_idx = ats
                            instructor_idx = qi[0]
                            
                    #   no: go to next T (ats) i.e. continue

                # TODO: satisfy HC 2: unique (I, T) in S
                # TODO: satisfy HC 1: unique (R, T) in S
            S.append(
                [room_idx, timeslot_idx, course_idx, instructor_idx])

    return np.array(S)


def is_unique_I_T(I, T, Sch):
    # TODO: return true if (I,T) does not exist in S
    pass


def get_free_room_at(Timeslot, Sch):
    # TODO: get free room at T
    no_free_room = True
    if no_free_room:
        return False

