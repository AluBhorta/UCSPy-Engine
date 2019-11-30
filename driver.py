import numpy as np
from models.models import Lecture, Course, Instructor, Room, Timeslot
from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS
from data.generate_random_schedule import generate_random_schedule
from fitness.encode_decode import encode, decode
from fitness.fitness import fitness, hard_penalty_multiplier
from fitness.constraints.hard_constraints import violates_hc1, violates_hc2, violates_hc3


def print_inputs():
    print("\nROOMS: (str room_id) \n", ROOMS)
    print("\nTIMESLOTS: (str timeslot_id) \n", TIMESLOTS)
    print("\nCOURSES: (str course_id, int num_of_lectures, int[] preferred_rooms)\n", COURSES)
    print("\nINSTRUCTORS: (str instuctor_id, int[] qualified_courses, int[] available_timeslots)\n", INSTRUCTORS)


def check_constraints(sch):
    hc1 = violates_hc1(sch)
    hc2 = violates_hc2(sch)
    hc3 = violates_hc3(sch)
    out = ""
    if not hc1:
        out += "yay, no VHC11"
    if not hc2:
        out += "\tyay, no VHC2!"
    if not hc3:
        out += "\tyay, no VHC3!"

    print(out)


def print_decoded_schedule(sch):
    for l in sch:
        print(decode(l))


def main():
    s = generate_random_schedule()
    for l in s:
        print(decode(l))


if __name__ == "__main__":
    main()
