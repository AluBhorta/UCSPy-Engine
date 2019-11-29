import numpy as np
from models.models import Lecture, Course, Instructor, Room, Timeslot
from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS
from data.generate_random_schedule import generate_random_schedule
from fitness.constraints.hard_constraints import violates_hc1, violates_hc2


def print_inputs():
    print("\nROOMS: (str room_id) \n", ROOMS)
    print("\nTIMESLOTS: (str timeslot_id) \n", TIMESLOTS)
    print("\nCOURSES: (str course_id, int num_of_lectures, int[] preferred_rooms)\n", COURSES)
    print("\nINSTRUCTORS: (str instuctor_id, int[] qualified_courses, int[] available_timeslots)\n", INSTRUCTORS)


def check_constraints():
    for i in range(100):
        s = generate_random_schedule()

        hc1 = violates_hc1(s)
        hc2 = violates_hc2(s)
        print("hc1: %d, hc2: %d" % (hc1, hc2))


def main():
    check_constraints()


if __name__ == "__main__":
    main()
