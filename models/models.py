class Room:
    def __init__(self, room_id):
        self.room_id = room_id

    def __repr__(self):
        return 'Room (Room-ID: %d)' % self.room_id


class Timeslot:
    def __init__(self, slot_id):
        self.slot_id = slot_id


class Course:
    def __init__(self, course_id, num_of_lectures, preferred_rooms):
        self.course_id = course_id
        self.num_of_lectures = num_of_lectures
        self.preferred_rooms = preferred_rooms
        

class Instructor:
    def __init__(self, instuctor_id, qualified_courses, available_timeslots):
        self.instuctor_id = instuctor_id
        self.qualified_courses = qualified_courses
        self.available_timeslots = available_timeslots
        

class Lecture:
    def __init__(self, encoded_lecture, room, timeslot, course, instructor):
        self.encoded_lecture = encoded_lecture
        self.room = room
        self.timeslot = timeslot
        self.course = course
        self.instructor = instructor
    
    def __repr__(self):
        return "Lecture: \n\tRoom: %s,\n\tTimeslot: %s,\n\tCourse: %s,\n\tInstructor: %s\n" % (
            self.room, self.timeslot, self.course, self.instructor
        )

# WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
