from typing import List


class Timeslot:
    _daily_slot_mapping = {
        0: '08:00-09:30',
        1: '09:40-11:10',
        2: '11:20-12:50',
        3: '12:50-13:40',
        4: '13:40-15:10',
        5: '15:20-16:50',
        6: '17:00-18:30',
        7: '18:30-20:00',
        8: '20:00-21:30',
    }

    def __init__(self, idx, weekday, daily_slot):
        self.idx = idx
        self.weekday = weekday
        self.daily_slot = daily_slot
        self.desc = self._generate_desc()

    def __str__(self):
        return f"""Timeslot - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""{self.__str__()}, 
            daily_slot: {self.daily_slot}
            \n
        """

    def _generate_desc(self):
        return f"{self.weekday} {self._daily_slot_mapping.get(self.daily_slot)}"


class Room:
    """Room

    a room with `allowed_courses == []` means all courses are allowed in that room.
    """

    def __init__(self, idx, desc, seat_capacity, allowed_courses=[]):
        self.idx = idx
        self.desc = desc
        self.seat_capacity = seat_capacity
        self.allowed_courses = allowed_courses

    def __str__(self):
        return f"""Room - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""{self.__str__()},
            seat_capacity: {self.seat_capacity},
            allowed_courses: {self.allowed_courses}
            \n        
        """


class Course:
    def __init__(self, idx, desc, num_of_sections, timeslots_per_class, classes_per_week, course_type):
        self.idx = idx
        self.desc = desc
        self.num_of_sections = num_of_sections
        self.timeslots_per_class = timeslots_per_class
        self.classes_per_week = classes_per_week
        self.course_type = course_type
        self.sections = self._generate_sections()

    def __str__(self):
        return f"""Course - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""
            {self.__str__()},
            num_of_sections: {self.num_of_sections},
            timeslots_per_class: {self.timeslots_per_class},
            classes_per_week: {self.classes_per_week},
            course_type: {self.course_type},
            sections: {self.sections}
            \n
        """

    def _generate_sections(self):
        return [Section(self, (i+1)) for i in range(self.num_of_sections)]


class Section:
    def __init__(self, course: Course, sec_number: int):
        self.course = course
        self.sec_number = sec_number

    def __repr__(self):
        return f'Section - course_idx: {self.course.idx}, section: {self.sec_number} \n'


class Instructor:
    def __init__(self, idx, desc, assigned_course_idxs, preferred_timeslot_idxs):
        self.idx = idx
        self.desc = desc
        self.assigned_course_idxs = assigned_course_idxs
        self.preferred_timeslot_idxs = preferred_timeslot_idxs

    def __str__(self):
        return f"""Instructor - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""
            {self.__str__()}, 
            assigned_course_idxs: {self.assigned_course_idxs}, 
            preferred_timeslot_idxs: {self.preferred_timeslot_idxs} 
            \n
        """


class CourseGroup:
    def __init__(self, idx, desc, courses, preferred_timeslot_idxs):
        self.idx = idx
        self.desc = desc
        self.courses = courses
        self.preferred_timeslot_idxs = preferred_timeslot_idxs

    def __str__(self):
        return f"CourseGroup - idx: {self.idx}, desc: {self.desc}"

    def __repr__(self):
        return f"""{self.__str__()},
            courses: {self.courses},
            preferred_timeslot_idxs: {self.preferred_timeslot_idxs}
            \n
        """


class StateManager:
    """State Manager

    Singleton Object used to hold & access all Schedule-Params (i.e. Rooms, Timeslots, Courses, Instructors, CourseGroups) and Sections.
    """

    def __init__(self, rooms: List[Room], timeslots: List[Timeslot], courses: List[Course], instructors: List[Instructor], course_groups: List[CourseGroup]):
        self.rooms = rooms
        self.timeslots = timeslots
        self.instructors = instructors
        self.courses = courses
        self.course_groups = course_groups
        self.sections = self._get_sections()
        self.num_of_daily_slots = len(Timeslot._daily_slot_mapping)

    def __repr__(self):
        return f"""StateManager - 
            ROOMS: {self.rooms},
            TIMESLOTS: {self.timeslots},
            INSTRUCTORS: {self.instructors},
            COURSES: {self.courses},
            COURSE_GROUPS: {self.course_groups},
            SECTIONS: {self.sections},
            \n
        """

    def _get_sections(self) -> List[Section]:
        sections = []
        for c in self.courses:
            sections.append(c.sections)
        return sections

    def get_room(self, room_idx):
        return self.rooms[room_idx]

    def get_timeslot(self, timeslot_idx):
        return self.timeslots[timeslot_idx]

    def get_course(self, course_idx):
        return self.courses[course_idx]

    def get_instructor(self, instructor_idx):
        return self.instructors[instructor_idx]


class Class:
    def __init__(self, timeslots: List[Timeslot], room: Room, section: Section, instructor: Instructor):
        self.timeslots = timeslots
        self.room = room
        self.section = section
        self.instructor = instructor


class Schedule:
    def __init__(self, classes: List[Class]):
        self.classes = classes


# TODO: implement hard and soft constraints as classes to extend the current fitness calculation more intuitively
# class HardConstraint:
#     def __init__(self):
#         pass


# class SoftConstraint:
#     def __init__(self):
#         pass
