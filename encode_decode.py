from models.models import Lecture
from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS

def decode(encoded_lecture: (int, int, int, int)) -> Lecture:
    """solution decoder"""
    return Lecture(
        encoded_lecture,
        ROOMS[encoded_lecture[0]],
        TIMESLOTS[encoded_lecture[1]],
        COURSES[encoded_lecture[2]],
        INSTRUCTORS[encoded_lecture[3]]
    )


def encode(lecture: Lecture) -> (int, int, int, int):
    """solution encoder"""
    return lecture.encoded_lecture


def _verify_encode_decode():
    print("(Room, Timeslot, Course, Instructor)")
    # generate a lecture
    l1 = (3, 4, 1, 0)
    print(l1)
    L1 = decode(l1)
    print(L1)
    l2 = encode(L1)
    print(l2)

