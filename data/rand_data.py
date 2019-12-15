# TODO: make a func that takes in the changeable variables and returns the genrated random inputs
import numpy as np

np.random.seed(69)


# main pararms to alter for randomization
NUM_OF_ROOMS = 20
NUM_OF_TIMELSOTS = 20
NUM_OF_COURSES = 10
NUM_OF_INSTRUCTORS = 20

# secondary params
MAX_NUM_OF_LECS_PER_COURSE = 2
MIN_NUM_OF_LECS_PER_COURSE = 1

MAX_NUM_OF_QUALIFIED_COURSES_PER_INSTRUCTOR = NUM_OF_COURSES * 0.9
MIN_NUM_OF_QUALIFIED_COURSES_PER_INSTRUCTOR = 2

R = NUM_OF_TIMELSOTS
MIN_AVAILABLE_TIMESLOTS_PER_INSTRUCTOR = 2

# SOFT CONSTRAINT PARAMS

MAX_NUM_OF_PREFFERED_ROOMS_PER_COURSE = NUM_OF_ROOMS * 0.9
MIN_NUM_OF_PREFFERED_ROOMS_PER_COURSE = 1

# new
MAX_NUM_OF_PREFFERED_ROOMS_PER_INSTRUCTOR = NUM_OF_ROOMS * 0.9
MIN_NUM_OF_PREFFERED_ROOMS_PER_INSTRUCTOR = 1

MAX_NUM_OF_PREFFERED_TIMESLOTS_PER_COURSE = NUM_OF_TIMELSOTS * 0.5
MIN_NUM_OF_PREFFERED_TIMESLOTS_PER_COURSE = 1

MAX_NUM_OF_PREFFERED_TIMESLOTS_PER_INSTRUCTOR = NUM_OF_TIMELSOTS * 0.5
MIN_NUM_OF_PREFFERED_TIMESLOTS_PER_INSTRUCTOR = 1

# (DO NOT MODIFY) inferred variables

MAX_LECS_PER_TIMESLOT = NUM_OF_ROOMS if NUM_OF_ROOMS < NUM_OF_INSTRUCTORS else NUM_OF_INSTRUCTORS
MAX_LECS_THAT_CAN_BE_OFFERED = MAX_LECS_PER_TIMESLOT * NUM_OF_TIMELSOTS

# inputs to the Engine

"""
(int room_idx, str room_desc)[]
"""
ROOMS = np.array([(
    i,
    "Room%d" % i
) for i in np.arange(NUM_OF_ROOMS)], dtype=object)
"""
(int timeslot_idx, str timeslot_desc)[]
"""
TIMESLOTS = np.array([(
    i,
    "Timeslot%d" % i
) for i in np.arange(NUM_OF_TIMELSOTS)], dtype=object)

"""
(int course_idx, str course_desc, int num_of_lectures, int[] preferred_rooms, int[] preferred_timeslots)[]
"""
COURSES = np.array([
    (
        i,
        "CSE%d" % i,
        np.random.randint(
            low=MIN_NUM_OF_LECS_PER_COURSE,
            high=MAX_NUM_OF_LECS_PER_COURSE+1
        ),
        np.random.randint(
            low=0,
            high=NUM_OF_ROOMS,
            size=np.random.randint(
                low=MIN_NUM_OF_PREFFERED_ROOMS_PER_COURSE,
                high=MAX_NUM_OF_PREFFERED_ROOMS_PER_COURSE+1
            )
        ),
        np.random.randint(
            low=0,
            high=NUM_OF_ROOMS,
            size=np.random.randint(
                low=MIN_NUM_OF_PREFFERED_TIMESLOTS_PER_COURSE,
                high=MAX_NUM_OF_PREFFERED_TIMESLOTS_PER_COURSE+1
            )
        )
    ) for i in np.arange(NUM_OF_COURSES)
])

"""
(int instuctor_idx, str instuctor_desc, int[] qualified_courses, int[] available_timeslots, int[] preferred_rooms, int[] preferred_timeslots)[]
"""
INSTRUCTORS = np.array([
    (
        i,
        "INSTRUCTOR%d" % i,
        list(set(
            np.random.choice(
                np.arange(NUM_OF_COURSES),
                size=np.random.randint(
                    low=MIN_NUM_OF_QUALIFIED_COURSES_PER_INSTRUCTOR,
                    high=MAX_NUM_OF_QUALIFIED_COURSES_PER_INSTRUCTOR+1
                )
            )
        )),
        list(set(
            np.random.choice(
                np.arange(NUM_OF_TIMELSOTS),
                size=np.random.randint(
                    low=MIN_AVAILABLE_TIMESLOTS_PER_INSTRUCTOR,
                    high=R+1
                )
            )
        )),
        np.random.randint(
            low=0,
            high=NUM_OF_ROOMS,
            size=np.random.randint(
                low=MIN_NUM_OF_PREFFERED_ROOMS_PER_INSTRUCTOR,
                high=MAX_NUM_OF_PREFFERED_ROOMS_PER_INSTRUCTOR+1
            )
        ),
        np.random.randint(
            low=0,
            high=NUM_OF_ROOMS,
            size=np.random.randint(
                low=MIN_NUM_OF_PREFFERED_TIMESLOTS_PER_INSTRUCTOR,
                high=MAX_NUM_OF_PREFFERED_TIMESLOTS_PER_INSTRUCTOR+1
            )
        )
    ) for i in np.arange(NUM_OF_INSTRUCTORS)
])


# sum of lectures of all courses
NUM_OF_LECS_BEING_OFFERED = COURSES[:, 2].sum()

# sanity check
if NUM_OF_LECS_BEING_OFFERED > MAX_LECS_THAT_CAN_BE_OFFERED:
    raise Exception(
        "ERROR! Max number of Lectures exceeded.\n" +
        "LECS_BEING_OFFERED: %d" % NUM_OF_LECS_BEING_OFFERED +
        ",\tMAX_LECS_THAT_CAN_BE_OFFERED: %d" % MAX_LECS_THAT_CAN_BE_OFFERED
    )
