from typing import List
from numpy import array


DAILY_SLOTS = [
    '08:00-09:30',
    '09:40-11:10',
    '11:20-12:50',
    '13:40-15:10',
    '15:20-16:50',
    '17:00-18:30',
    '18:30-21:30',
]

DAY_CODES = [
    'ST',
    'MW',
    'S',
    'T',
    'M',
    'W',
    'R',
]


class Timeslot:
    def __init__(self, idx, day_code, daily_slot, conflicts_with_idxs):
        self.idx = idx
        self.day_code = day_code
        self.daily_slot = daily_slot
        self.conflicts_with_idxs = conflicts_with_idxs
        self.desc = self.__str__()

    def __str__(self):
        return f"""{self.day_code} {self.daily_slot}"""

    def __repr__(self):
        return f"""Timeslot - idx: {self.idx}, 
            {self.__str__()},
            conflicts_with_idxs: {self.conflicts_with_idxs}
            \n
        """


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
    def __init__(self, idx, desc, num_of_sections, lectures_per_week, course_type):
        self.idx = idx
        self.desc = desc
        self.num_of_sections = num_of_sections
        self.lectures_per_week = lectures_per_week
        self.course_type = course_type
        self.sections = self._generate_sections()
        self.credits = self._get_credits()

    def _get_credits(self):
        return 1 if self.course_type.lower() == "lab" else 3

    def __str__(self):
        return f"""Course - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""
            {self.__str__()},
            num_of_sections: {self.num_of_sections},
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
        return f'''Section - course_idx: {self.course.idx}, 
            section: {self.sec_number}
            \n
        '''


class Instructor:
    def __init__(self, idx, desc, assigned_course_idxs, preferred_timeslot_idxs, min_credit_req):
        self.idx = idx
        self.desc = desc
        self.assigned_course_idxs = assigned_course_idxs
        self.preferred_timeslot_idxs = preferred_timeslot_idxs
        self.min_credit_req = min_credit_req

    def __str__(self):
        return f"""Instructor - idx: {self.idx}, desc: {self.desc}"""

    def __repr__(self):
        return f"""
            {self.__str__()}, 
            assigned_course_idxs: {self.assigned_course_idxs}, 
            preferred_timeslot_idxs: {self.preferred_timeslot_idxs} 
            min_credit_req: {self.min_credit_req} 
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


class Class:
    def __init__(
        self,
        section: Section,
        instructor: Instructor,
        room: Room,
        timeslot: Timeslot
    ):
        self.section = section
        self.instructor = instructor
        self.room = room
        self.timeslot = timeslot

    def __str__(self):
        return f"""Class: ({self.section.course.desc, self.section.sec_number, self.instructor.desc, self.room.desc, self.timeslot })\n"""

    def __repr__(self):
        return f"""### CLASS ###
            Course:\t{self.section.course}
            Section:\t{self.section}
            Instructor:\t{self.instructor}
            Room:\t{self.room}
            Timeslot:\t{self.timeslot}
            \n
        """


class Schedule:
    def __init__(self, classes: List[Class]):
        self.classes = classes

    def __str__(self):
        return self.to_tsv()

    def flatten(self):
        schedule = self.get_numeric_repr()
        a = array([item for _cls in schedule for item in _cls])
        # a.shape = (1,len(a))
        return a

    def get_numeric_repr(self):
        """ NOTE: returns schedule in np.array<(C, S, I, R, T)> format """
        return array([(
            c.section.course.idx,
            c.section.sec_number,
            c.instructor.idx,
            c.room.idx,
            c.timeslot.idx
        ) for c in self.classes])

    def to_csv(self):
        """ to human-readable csv format """
        out = "Course,Section,Instructor,Room,Timeslot\n"
        for c in self.classes:
            out += f"{c.section.course.desc},{c.section.sec_number},{c.instructor.desc},{c.room.desc},{c.timeslot.desc}\n"
        return out

    def to_tsv(self):
        """ to human-readable csv format """
        out = "Course\tSection\tInstructor\tRoom\tTimeslot\n"
        for c in self.classes:
            out += f"{c.section.course.desc}\t{c.section.sec_number}\t{c.instructor.desc}\t{c.room.desc}\t{c.timeslot.desc}\n"
        return out

    def to_num_csv(self):
        """ to numeric csv format """
        out = "Course,Section,Instructor,Room,Timeslot\n"
        nr = self.get_numeric_repr()
        for c in nr:
            out += f"{c[0]},{c[1]},{c[2]},{c[3]},{c[4]}\n"
        return out


class ScheduleParam:
    def __init__(self, rooms: List[Room], timeslots: List[Timeslot], courses: List[Course], instructors: List[Instructor], course_groups: List[CourseGroup]):
        self.rooms = rooms
        self.timeslots = timeslots
        self.instructors = instructors
        self.courses = courses
        self.course_groups = course_groups


class StateManager:
    """State Manager

    Singleton used to hold & access state of UCSP.
    """

    def __init__(self, schedule_param: ScheduleParam, HARD_CONSTRAINTS, SOFT_CONSTRAINTS, fit_func, generate_random_schedule):
        self.rooms = schedule_param.rooms
        self.timeslots = schedule_param.timeslots
        self.instructors = schedule_param.instructors
        self.courses = schedule_param.courses
        self.course_groups = schedule_param.course_groups
        self.sections = self._get_sections()
        self.daily_slots = DAILY_SLOTS
        self.num_of_daily_slots = len(DAILY_SLOTS)
        self.day_codes = DAY_CODES
        self._fit_func = fit_func
        self.hard_constraints = HARD_CONSTRAINTS
        self.soft_constraints = SOFT_CONSTRAINTS
        self.generate_schedule = self._get_generate_schedule(
            generate_random_schedule)

    def _get_generate_schedule(self, grs_func):
        def f() -> Schedule:
            return grs_func(self)
        return f

    def _get_theory_lab_course_idx_paris(self):
        """ NOTE: for this to work, the Lab course should should be directly after its corresponding Theory course  in the `courses.csv` schedule_param
        TODO: replace the indexing strategy with a dedicated parameter in Course instance (e.g. C.lab_of_course_idx)
        """
        pairs = []
        for crs in self.courses:
            if crs.course_type.lower() == "lab":
                pairs.append((crs.idx-1, crs.idx))
        return pairs

    def fitness(self, sch: Schedule, _inspect=False) -> float:
        return self._fit_func(sch, self, _inspect)

    # def fitness_error(self, sch: Schedule, _inspect=False) -> float:
    #     f = self.fitness(sch, _inspect)
    #     return

    def flat_fitness(self, sch, class_dimension=5):
        sch.shape = (len(self.sections), class_dimension)
        sch = self.numeric_to_sch(sch)
        return self.fitness(sch)

    def flat_fitness_array(self, sch_arr, class_dimension=5):
        return array([self.flat_fitness(sch) for sch in sch_arr])

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

        NOTE: `num_repr` is of type np.array<(C, S, I, R, T)>
        """
        return Schedule(
            classes=[(
                Class(
                    Section(self.get_course(i[0]), i[1]),
                    self.get_instructor(i[2]),
                    self.get_room(i[3]),
                    self.get_timeslot(i[4])
                )
            ) for i in num_repr]
        )

    def _get_sections(self) -> List[Section]:
        sections = []
        for c in self.courses:
            sections.extend(c.sections)
        return sections

    def get_room(self, room_idx):
        return self.rooms[int(room_idx)]

    def get_timeslot(self, timeslot_idx):
        return self.timeslots[int(timeslot_idx)]

    def get_course(self, course_idx):
        return self.courses[int(course_idx)]

    def get_instructor(self, instructor_idx):
        return self.instructors[int(instructor_idx)]

    def get_course_group(self, course_group_idx):
        return self.course_groups[int(course_group_idx)]
