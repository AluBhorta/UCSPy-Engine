import numpy as np
from models.models import Lecture, Course, Instructor, Room, Timeslot
from data.rand_data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS, generate_random_schedule


# L = (R[i], T[j], C[k], I[p])

def decode(encoded_lecture) -> Lecture:
    return Lecture(
        encoded_lecture,
        ROOMS[encoded_lecture[0]],
        TIMESLOTS[encoded_lecture[1]], 
        COURSES[encoded_lecture[2]], 
        INSTRUCTORS[encoded_lecture[3]]
    )


def encode(lecture: Lecture) -> (int, int, int, int):
    return lecture.encoded_lecture


def print_input():
    print("\nROOMS: (str room_id) \n",ROOMS)
    print("\nTIMESLOTS: (str timeslot_id) \n",TIMESLOTS)
    print("\nCOURSES: (str course_id, int num_of_lectures, int[] preferred_rooms)\n",COURSES)
    print("\nINSTRUCTORS: (str instuctor_id, int[] qualified_courses, int[] available_timeslots)\n",INSTRUCTORS)


def main():
    print("(Room, Timeslot, Course, Instructor)")
    
    # generate a lecture
    l1 = (3,4,1,0)
    print(l1)

    L1 = decode(l1)
    print(L1)
    
    l2 = encode(L1)
    print(l2)

if __name__ == "__main__":
    print_input()
    