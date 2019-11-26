import numpy as np
from models.models import Lecture, Course, Instructor, Room, Timeslot
from data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS


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


if __name__ == "__main__":
    print("(Room, Timeslot, Course, Instructor)")
    
    # generate a lecture
    l1 = (3,4,1,0)
    
    print(l1)

    L1 = decode(l1)
    print(L1)
    
    l2 = encode(L1)
    print(l2)

