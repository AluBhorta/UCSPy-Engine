class Room:
    def __init__(self, room_id):
        self.room_id = room_id


class Course:
    def __init__(self, num_of_lectures, preferred_rooms):
        self.num_of_lectures = num_of_lectures
        self.preferred_rooms = preferred_rooms
        

class Instructor:
    def __init__(self, qualified_courses, available_timeslots):
        self.qualified_courses = qualified_courses
        self.available_timeslots = available_timeslots
        

class Timeslot:
    def __init__(self, weekly_timeslots):
        self.weekly_timeslots = weekly_timeslots


class Lecture:
    def __init__(self, encoded_lecture, room, timeslot, course, instructor):
        self.encoded_lecture = encoded_lecture
        self.room = room
        self.timeslot = timeslot
        self.course = course
        self.instructor = instructor
    
    def __str__(self):
        return "Lecture (Room: %s, Timeslot: %s, Course: %s, Instructor: %s)" % (
            self.room, self.timeslot, self.course, self.instructor
        )

# WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]