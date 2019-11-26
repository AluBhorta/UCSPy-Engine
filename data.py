import numpy as np

np.random.seed(69)

NUM_OF_ROOMS = 10
NUM_OF_TIMELSOTS = 20
NUM_OF_COURSES = 10
NUM_OF_INSTRUCTORS = 5
MAX_NUM_OF_LECS_PER_COURSE = 5
MAX_NUM_OF_PREFFERED_ROOMS = NUM_OF_ROOMS/2
MAX_NUM_OF_QUALIFIED_COURSES = NUM_OF_COURSES/2


ROOMS = np.array(["Room-%d"%i for i in np.arange(NUM_OF_ROOMS)])

TIMESLOTS = np.array(["Timeslot-%d"%i for i in np.arange(NUM_OF_TIMELSOTS)])

"""
(int course_id, int num_of_lectures, int[] preferred_rooms)[]
"""
COURSES = np.array([
  (
    "CSE%d"%i, 
    np.random.randint(low=1, high=MAX_NUM_OF_LECS_PER_COURSE), 
    np.random.randint(low=0, high=NUM_OF_ROOMS+1, size=np.random.randint(NUM_OF_ROOMS/2))
  ) for i in np.arange(NUM_OF_COURSES)
])

"""
(int instuctor_id, int[] qualified_courses, int[] available_timeslots)[]
"""
INSTRUCTORS = np.array([
  (
    "INSTRUCTOR%d"%i,
    list(set(
      np.random.choice(
        np.arange(NUM_OF_COURSES),
        size=np.random.randint(low=1, high=MAX_NUM_OF_QUALIFIED_COURSES)
      )
    )),
    list(set(
      np.random.choice(
        np.arange(NUM_OF_TIMELSOTS),
        size=np.random.randint(low=1, high=NUM_OF_TIMELSOTS)
      )
    )),
  ) for i in np.arange(NUM_OF_INSTRUCTORS)
])

