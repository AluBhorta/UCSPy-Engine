"""
to import:
    COURSES, 
    INSTRUCTORS, 
    ROOMS, 
    TIMESLOTS, 
    NUM_OF_LECS_BEING_OFFERED
    NUM_OF_ROOMS, 
    NUM_OF_TIMELSOTS, 
    NUM_OF_COURSES, 
    NUM_OF_INSTRUCTORS, 

"""

"""For random generated data"""
# from data.rand_data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS, NUM_OF_LECS_BEING_OFFERED, NUM_OF_ROOMS, NUM_OF_TIMELSOTS, NUM_OF_COURSES, NUM_OF_INSTRUCTORS


"""For data parsed from CSV"""
from data.input_as_csv.parse_csv import parse_csv_from
ROOMS, TIMESLOTS, COURSES, INSTRUCTORS, NUM_OF_ROOMS, NUM_OF_TIMELSOTS, NUM_OF_COURSES, NUM_OF_INSTRUCTORS, NUM_OF_LECS_BEING_OFFERED, MAX_LECS_PER_TIMESLOT = parse_csv_from(
    "data/input_as_csv/" + "iub/")


