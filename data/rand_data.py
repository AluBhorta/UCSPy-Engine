# TODO: make a func that takes in the changeable variables and returns the genrated random inputs
import numpy as np

np.random.seed(69)

# vairables to alter for randomization

NUM_OF_ROOMS = 10
NUM_OF_TIMELSOTS = 20
NUM_OF_COURSES = 10
NUM_OF_INSTRUCTORS = 8

MAX_NUM_OF_LECS_PER_COURSE = 5
MAX_NUM_OF_PREFFERED_ROOMS = NUM_OF_ROOMS/2
MAX_NUM_OF_QUALIFIED_COURSES_PER_INSTRUCTOR = NUM_OF_COURSES/2

# (DO NOT MODIFY) inferred variables

MAX_LECS_PER_TIMESLOT = NUM_OF_ROOMS if NUM_OF_ROOMS < NUM_OF_INSTRUCTORS else NUM_OF_INSTRUCTORS
MAX_LECS_THAT_CAN_BE_OFFERED = MAX_LECS_PER_TIMESLOT * NUM_OF_TIMELSOTS

# inputs to the Engine

ROOMS = np.array(["Room-%d" % i for i in np.arange(NUM_OF_ROOMS)])

TIMESLOTS = np.array(["Timeslot-%d" % i for i in np.arange(NUM_OF_TIMELSOTS)])

"""
(str course_id, int num_of_lectures, int[] preferred_rooms)[]
"""
COURSES = np.array([
    (
        "CSE%d" % i,
        np.random.randint(low=1, high=MAX_NUM_OF_LECS_PER_COURSE),
        np.random.randint(low=0, high=NUM_OF_ROOMS+1,
                          size=np.random.randint(MAX_NUM_OF_PREFFERED_ROOMS))
    ) for i in np.arange(NUM_OF_COURSES)
])

"""
(str instuctor_id, int[] qualified_courses, int[] available_timeslots)[]
"""
INSTRUCTORS = np.array([
    (
        "INSTRUCTOR%d" % i,
        list(set(
            np.random.choice(
                np.arange(NUM_OF_COURSES),
                size=np.random.randint(
                    low=1,
                    high=MAX_NUM_OF_QUALIFIED_COURSES_PER_INSTRUCTOR
                )
            )
        )),
        list(set(
            np.random.choice(
                np.arange(NUM_OF_TIMELSOTS),
                size=np.random.randint(
                    low=1,
                    high=NUM_OF_TIMELSOTS
                )
            )
        )),
    ) for i in np.arange(NUM_OF_INSTRUCTORS)
])


# sum of lectures of all courses
LECS_BEING_OFFERED = COURSES[:, 1].sum()

# sanity check
if LECS_BEING_OFFERED > MAX_LECS_THAT_CAN_BE_OFFERED:
    raise Exception(
        "ERROR! Max number of Lectures exceeded.\n" +
        "LECS_BEING_OFFERED: %d" % LECS_BEING_OFFERED +
        ",\tMAX_LECS_THAT_CAN_BE_OFFERED: %d" % MAX_LECS_THAT_CAN_BE_OFFERED
    )
