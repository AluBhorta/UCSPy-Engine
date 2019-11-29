import numpy as np
from data.data import NUM_OF_ROOMS, NUM_OF_TIMELSOTS, NUM_OF_COURSES, NUM_OF_INSTRUCTORS, LECS_BEING_OFFERED



def generate_random_schedule():     # generates a random schedule
    # (Room, Timeslot, Course, Instructor)[]
    return np.array([
        (
            np.random.randint(NUM_OF_ROOMS),
            np.random.randint(NUM_OF_TIMELSOTS),
            np.random.randint(NUM_OF_COURSES),
            np.random.randint(NUM_OF_INSTRUCTORS)
        ) for i in np.arange(LECS_BEING_OFFERED)
    ])
