from models.models import Lecture
from data.data import COURSES, INSTRUCTORS, ROOMS, TIMESLOTS
from data.generate_random_schedule import generate_random_schedule


def _decode(encoded_lecture: (int, int, int, int)) -> Lecture:
    """DEPRICATED"""
    return Lecture(
        encoded_lecture,
        ROOMS[encoded_lecture[0]],
        TIMESLOTS[encoded_lecture[1]],
        COURSES[encoded_lecture[2]],
        INSTRUCTORS[encoded_lecture[3]]
    )


def _encode(lecture: Lecture) -> (int, int, int, int):
    """DEPRICATED"""
    return lecture.encoded_lecture

#  Decoded_Lecture: (Room, Timeslot, Course, Instructor)
# (
#   Room:       (str room_id),
#   Timeslot:   (str timeslot_id),
#   Course:     (str course_id, int num_of_lectures, int[] preferred_rooms),
#   Instructor: (str instuctor_id, int[] qualified_courses, int[] available_timeslots)
# )

def decode(encoded_lecture):
    """solution decoder"""
    return (
        ROOMS[encoded_lecture[0]],
        TIMESLOTS[encoded_lecture[1]],
        COURSES[encoded_lecture[2]],
        INSTRUCTORS[encoded_lecture[3]]
    )


def encode(decoded_lecture):
    """solution encoder"""
    room_id         =   int(decoded_lecture[0][4:])
    timeslot_id     =   int(decoded_lecture[1][8:])
    course_id       =   int(decoded_lecture[2][0][3:])
    instructor_id   =   int(decoded_lecture[3][0][10:])

    return [room_id, timeslot_id, course_id, instructor_id]



def _verify_encode_decode():
    print("(Room, Timeslot, Course, Instructor)")
    # generate a lecture
    s = generate_random_schedule()
    for lec in s:
        de_lec = decode(lec)
        print(lec)
        print(de_lec)

