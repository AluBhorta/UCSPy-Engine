from models.models import Lecture
from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS
from data.generate_random_schedule import generate_random_schedule

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
    s = generate_random_schedule()
    for lec in s:
        de_lec = decode(lec)
        print(lec)
        print(de_lec)


