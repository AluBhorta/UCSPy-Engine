
'''Encoded_Lecture: (Room, Timeslot, Course, Instructor)
    (int room_idx, int timeslot_idx, int course_idx, int instructor_id)
'''

'''Decoded_Lecture: (Room, Timeslot, Course, Instructor)
(
  Room:       
    (int room_idx, str room_desc) 
  Timeslot:
    (int timeslot_idx, str timeslot_desc) 
  Course:
    (int course_idx, str course_desc, int num_of_lectures, int[] preferred_rooms, int[] preferred_timeslots)
  Instructor:
   (int instuctor_idx, str instuctor_desc, int[] qualified_courses, int[] available_timeslots, int[] preferred_rooms, int[] preferred_timeslots)
)
'''


class Timeslot:
    def __init__(self, idx, desc):
        self.idx = idx
        self.desc = desc

    def __repr__(self):
        return f"""Timeslot - idx: {self.idx}, desc: {self.desc}"""


class Room:
    def __init__(self, idx, desc, allowed_courses="*"):
        self.idx = idx
        self.desc = desc
        self.allowed_courses = allowed_courses

    def __repr__(self):
        return f"""Room - idx: {self.idx}, desc: {self.desc}"""


class Course:
    def __init__(self, idx, desc, num_of_lectures, preferred_rooms, preferred_timeslots):
        self.idx = idx
        self.desc = desc
        self.num_of_lectures = num_of_lectures
        self.preferred_rooms = preferred_rooms
        self.preferred_timeslots = preferred_timeslots

    def __str__(self):
        return f"""Course - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""{self.__str__()}, num_of_lecs: {self.num_of_lectures}, preferred_rooms: {self.preferred_rooms}, preferred_timeslots: {self.preferred_timeslots}"""


class Instructor:
    def __init__(self, idx, desc, qualified_courses, available_in_timeslots, preferred_rooms, preferred_timeslots):
        self.idx = idx
        self.desc = desc
        self.qualified_courses = qualified_courses
        self.available_in_timeslots = available_in_timeslots
        self.preferred_rooms = preferred_rooms
        self.preferred_timeslots = preferred_timeslots

    def __str__(self):
        return f"""Instructor - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""{self.__str__()}, qualified_courses: {self.qualified_courses}, available_in_timeslots: {self.available_in_timeslots}, preferred_rooms: {self.preferred_rooms}, preferred_timeslots: {self.preferred_timeslots} """


class Lecture:
    def __init__(self, room_idx, timeslot_idx, course_idx, instructor_idx):
        self.room_idx = room_idx
        self.timeslot_idx = timeslot_idx
        self.course_idx = course_idx
        self.instructor_idx = instructor_idx

    def __str__(self):
        return str(self.encoded())

    def __repr__(self):
        return f"""Lecture - room_idx: {self.room_idx}, timeslot_idx: {self.timeslot_idx}, course_idx: {self.course_idx}, instructor_idx: {self.instructor_idx} """

    def decoded(self):
        # R = Room(self.room_idx, )
        # allow global DAO or pass it around through function args

        pass

    def encoded(self):
        return (self.room_idx, self.timeslot_idx, self.course_idx, self.instructor_idx)


class Schedule:
    def __init__(self, lectures):
        self.lectures = lectures
        self.lecture_count = len(lectures)

    def __str__(self):
        return str(self.lectures)


class DataAccessObject:
    """Data Access Object (DAO) 

    Singleton Object used to hold/access all input components (i.e. Rooms, Timeslots, Courses, Instructors) and convert components to/from indices (e.g. get Room instance using room_idx, if it exists).
    """

    def __init__(self, rooms, timeslots, courses, instructors):
        self.rooms = rooms
        self.timeslots = timeslots
        self.courses = courses
        self.instructors = instructors

    def get_room(self, room_idx):
        return self.rooms[room_idx]

    def get_timeslot(self, timeslot_idx):
        return self.timeslots[timeslot_idx]

    def get_course(self, course_idx):
        return self.courses[course_idx]

    def get_instructor(self, instructor_idx):
        return self.instructors[instructor_idx]


class HardConstraint:
    def __init__(self):
        pass


class SoftConstraint:
    def __init__(self):
        pass


WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
