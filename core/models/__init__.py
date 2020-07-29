from typing import List
from numpy import array

DAILY_SLOT_MAPPING = {
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


class Timeslot:
    def __init__(self, idx, weekday, daily_slot):
        self.idx = idx
        self.weekday = weekday
        self.daily_slot = daily_slot
        self.desc = self._generate_desc()

    def __str__(self):
        return f"""Timeslot - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""{self.__str__()}, daily_slot: {self.daily_slot} ;
        """

    def _generate_desc(self):
        return f"{self.weekday}: {DAILY_SLOT_MAPPING.get(self.daily_slot)}"


class Room:
    """Room

    a room with `allowed_course_idxs == []` means all courses are allowed in that room.
    """

    def __init__(self, idx, desc, seat_capacity, allowed_course_idxs=[]):
        self.idx = idx
        self.desc = desc
        self.seat_capacity = seat_capacity
        self.allowed_course_idxs = allowed_course_idxs

    def __str__(self):
        return f"""Room - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""{self.__str__()},
            seat_capacity: {self.seat_capacity},
            allowed_course_idxs: {self.allowed_course_idxs}
            \n        
        """


class Course:
    def __init__(self, idx, desc, num_of_sections, timeslots_per_lecture, lectures_per_week, course_type):
        self.idx = idx
        self.desc = desc
        self.num_of_sections = num_of_sections
        self.timeslots_per_lecture = timeslots_per_lecture
        self.lectures_per_week = lectures_per_week
        self.course_type = course_type
        self.sections = self._generate_sections()

    def __str__(self):
        return f"""Course - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""
            {self.__str__()},
            num_of_sections: {self.num_of_sections},
            timeslots_per_lecture: {self.timeslots_per_lecture},
            lectures_per_week: {self.lectures_per_week},
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
        return f'Section - course_idx: {self.course.idx}, section: {self.sec_number}'


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
    def __init__(self, idx, desc, course_idxs: List[Course], preferred_timeslot_idxs: List[int]):
        self.idx = idx
        self.desc = desc
        self.course_idxs = course_idxs
        self.preferred_timeslot_idxs = preferred_timeslot_idxs

    def __str__(self):
        return f"CourseGroup - idx: {self.idx}, desc: {self.desc}"

    def __repr__(self):
        return f"""{self.__str__()},
            course_idxs: {self.course_idxs},
            preferred_timeslot_idxs: {self.preferred_timeslot_idxs}
            \n
        """


class StateManager:
    """State Manager

    Singleton Object used to hold & access all Schedule-Params (i.e. Rooms, Timeslots, Courses, Instructors, CourseGroups) and Sections.
    """

    def __init__(self, rooms: List[Room], timeslots: List[Timeslot], courses: List[Course], instructors: List[Instructor], course_groups: List[CourseGroup], fit_func):
        self.rooms = rooms
        self.timeslots = timeslots
        self.instructors = instructors
        self.courses = courses
        self.course_groups = course_groups
        self.sections = self._get_sections()
        self.num_of_daily_slots = len(DAILY_SLOT_MAPPING)
        self.fitness = fit_func

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

    def numeric_to_sch(self, num_repr):
        """ 
        returns a Schedule from `num_repr`

        NOTE: `num_repr` is of type np.array<(C, S, I, R, Ts[])>
        """
        return Schedule(
            classes=[(
                Class(
                    Section(self.get_course(i[0]), i[1]),
                    self.get_instructor(i[2]),
                    self.get_room(i[3]),
                    [self.get_timeslot(j) for j in i[4]]
                )
            ) for i in num_repr],
            course_groups=self.course_groups
        )

    def _get_sections(self) -> List[Section]:
        sections = []
        for c in self.courses:
            sections.extend(c.sections)
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
    def __init__(
        self,
        section: Section,
        instructor: Instructor,
        room: Room,
        timeslots: List[Timeslot]
    ):
        self.section = section
        self.instructor = instructor
        self.room = room
        self.timeslots = timeslots

    def __str__(self):
        return f"""Class: ({self.section.course.desc, self.section.sec_number, self.instructor.desc, self.room.desc, str([t.desc for t in self.timeslots])})\n"""

    def __repr__(self):
        return f"""### CLASS ###
            Course:\t{self.section.course}
            Section:\t{self.section}
            Instructor:\t{self.instructor}
            Room:\t{self.room}
            Timeslots:\t{self.timeslots}
            \n
        """


class Schedule:
    def __init__(self, classes: List[Class], course_groups: List[CourseGroup]):
        self.classes = classes
        self.course_groups = course_groups

    def __str__(self):
        return self.to_csv()
        # return f"""
        #     Classes:\n {self.classes}
        #     \n
        #     CourseGroups:\n {self.course_groups}
        # """

    def get_numeric_repr(self):
        """ NOTE: returns schedule in np.array<(C, S, I, R, Ts[])> format """
        return array([(
            c.section.course.idx,
            c.section.sec_number,
            c.instructor.idx,
            c.room.idx,
            array([t.idx for t in c.timeslots]),
        ) for c in self.classes])

    def to_csv(self):
        """ to human-readable csv format """
        out = "Course,Section,Instructor,Room,Timeslots\n"
        for c in self.classes:
            ts = '"'
            l = len(c.timeslots)
            for i in range(l):
                if i == l-1:
                    ts += c.timeslots[i].desc + '"'
                else:
                    ts += c.timeslots[i].desc + ','

            out += f"{c.section.course.desc},{c.section.sec_number},{c.instructor.desc},{c.room.desc},{ts}\n"

        return out

    def to_num_csv(self):
        """ To numeric csv format """
        out = "Course,Section,Instructor,Room,Timeslots\n"
        nr = self.get_numeric_repr()
        for c in nr:
            ts = '"'
            l = len(c[4])
            for i in range(l):
                if i == l-1:
                    ts += str(c[4][i]) + '"'
                else:
                    ts += str(c[4][i]) + ','

            out += f"{c[0]},{c[1]},{c[2]},{c[3]},{ts}\n"

        return out
