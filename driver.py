import numpy as np
from models.models import Lecture, Course, Instructor, Room, Timeslot

ROOMS = ["R1", "R2", "R3"]

TIMESLOTS = [1, 2, 3, 4]

COURSES = ["CSC101", "CSC102", "MAT301"]

INSTRUCTORS = ["I1", "I2", "I3"]


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


l1 = (1,1,2,1)

L1 = decode(l1)
print(L1)
l2 = encode(L1)
print(l2)

