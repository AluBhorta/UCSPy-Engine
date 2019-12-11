from models.models import Lecture
from data.data import ROOMS, TIMESLOTS, COURSES, INSTRUCTORS


'''Encoded_Lecture: (Room, Timeslot, Course, Instructor)
    (int room_id, int timeslot_id, int course_id, int instructor_id)
'''


def decode(encoded_lecture):
    """solution decoder"""
    return (
        ROOMS[encoded_lecture[0]],
        TIMESLOTS[encoded_lecture[1]],
        COURSES[encoded_lecture[2]],
        INSTRUCTORS[encoded_lecture[3]]
    )


'''Decoded_Lecture: (Room, Timeslot, Course, Instructor)
(
  Room:       
    (int room_id, str room_desc) 
  Timeslot:
    (int timeslot_id, str timeslot_desc) 
  Course:
    (int course_id, str course_desc, int num_of_lectures, int[] preferred_rooms, int[] preferred_timeslots)
  Instructor:
   (int instuctor_id, str instuctor_desc, int[] qualified_courses, int[] available_timeslots, int[] preferred_rooms, int[] preferred_timeslots)
)
'''


def encode(decoded_lecture):
    """solution encoder"""
    room_id         = decoded_lecture[0][0]
    timeslot_id     = decoded_lecture[1][0]
    course_id       = decoded_lecture[2][0]
    instructor_id   = decoded_lecture[3][0]

    return [room_id, timeslot_id, course_id, instructor_id]
