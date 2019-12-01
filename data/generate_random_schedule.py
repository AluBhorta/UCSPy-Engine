import numpy as np
from data.data import ROOMS, TIMESLOTS, COURSES, INSTRUCTORS, NUM_OF_ROOMS, NUM_OF_TIMELSOTS, NUM_OF_COURSES, NUM_OF_INSTRUCTORS, NUM_OF_LECS_BEING_OFFERED
from fitness.encode_decode import encode, decode


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
    '''
    satisfies hard constraint 3 & 4 first, when possible
    '''
    Schedule = []

    for Course in COURSES:
        course_id = Course[0]

        qualified_instructors = []
        for Instructor in INSTRUCTORS:
            if course_id in Instructor[2]:
                qualified_instructors.append(Instructor[0])

        if not qualified_instructors:
            raise Exception(
                "Error! No qualified instructors for Course %s found!" % Course[1])

        for lec_i in range(Course[2]):
            instructor_id = np.random.choice(qualified_instructors)
            timeslot_id = np.random.choice(INSTRUCTORS[instructor_id][3])
            room_id = np.random.choice(Course[3])   # optimizes for soft_constraint_1 as well
            # np.random.randint(NUM_OF_ROOMS)       # worse violations

            Schedule.append([room_id, timeslot_id, course_id, instructor_id])

    return np.array(Schedule)
