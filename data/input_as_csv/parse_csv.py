from pandas import read_csv
import numpy as np


def str_to_array(str_values):
    return np.array([int(i) for i in str_values.split(",")])


def parse_csv_from(_dir="data/input_as_csv/" + "iub/"):
    R_DF = read_csv(_dir + "Rooms.csv")
    T_DF = read_csv(_dir + "Timeslots.csv")
    C_DF = read_csv(_dir + "Courses.csv")
    I_DF = read_csv(_dir + "Instructors.csv")

    ROOMS = R_DF.to_numpy()
    TIMESLOTS = T_DF.to_numpy()
    COURSES = C_DF.to_numpy()
    INSTRUCTORS = I_DF.to_numpy()

    # parse str cols: 3,4 - for Courses
    for i in range(len(COURSES)):
        COURSES[i][3] = str_to_array(COURSES[i][3])
        COURSES[i][4] = str_to_array(COURSES[i][4])

    # parse str cols: 2,3,4,5 - for Instructors
    for i in range(len(INSTRUCTORS)):
        INSTRUCTORS[i][2] = str_to_array(INSTRUCTORS[i][2])
        INSTRUCTORS[i][3] = str_to_array(INSTRUCTORS[i][3])
        INSTRUCTORS[i][4] = str_to_array(INSTRUCTORS[i][4])
        INSTRUCTORS[i][5] = str_to_array(INSTRUCTORS[i][5])

    '''
    Implied
    '''
    NUM_OF_ROOMS = len(ROOMS)
    NUM_OF_TIMELSOTS = len(TIMESLOTS)
    NUM_OF_COURSES = len(COURSES)
    NUM_OF_INSTRUCTORS = len(INSTRUCTORS)

    NUM_OF_LECS_BEING_OFFERED = COURSES[:, 2].sum()

    MAX_LECS_PER_TIMESLOT = NUM_OF_ROOMS if NUM_OF_ROOMS < NUM_OF_INSTRUCTORS else NUM_OF_INSTRUCTORS
    MAX_LECS_THAT_CAN_BE_OFFERED = MAX_LECS_PER_TIMESLOT * NUM_OF_TIMELSOTS
    # sanity check
    if NUM_OF_LECS_BEING_OFFERED > MAX_LECS_THAT_CAN_BE_OFFERED:
        raise Exception(
            "ERROR! Max number of Lectures exceeded.\n" +
            "LECS_BEING_OFFERED: %d" % NUM_OF_LECS_BEING_OFFERED +
            ",\tMAX_LECS_THAT_CAN_BE_OFFERED: %d" % MAX_LECS_THAT_CAN_BE_OFFERED
        )

    return ROOMS, TIMESLOTS, COURSES, INSTRUCTORS, NUM_OF_ROOMS, NUM_OF_TIMELSOTS, NUM_OF_COURSES, NUM_OF_INSTRUCTORS, NUM_OF_LECS_BEING_OFFERED, MAX_LECS_PER_TIMESLOT
