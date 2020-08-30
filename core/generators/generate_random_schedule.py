from typing import List
import random

from core.models import StateManager, Schedule, Class, Section, Course, Instructor, Timeslot, Room


def generate_random_schedule(state: StateManager) -> Schedule:
    '''Random schedule generator
    '''
    classes = []

    for C in state.courses:
        assigned_instructors = _get_assigned_Instructors_for(C, state)

        for sec_i in range(C.num_of_sections):
            instructor, timeslot, room = _get_unique_Instr_Timeslot_Room(
                assigned_instructors, C, classes, state)

            section = Section(C, sec_i+1)
            classes.append(Class(section, instructor, room, timeslot))

    return Schedule(classes)


def _get_assigned_Instructors_for(course: Course, state: StateManager):
    INSTRUCTORS = state.instructors

    assigned_instructors = []
    for I in INSTRUCTORS:
        if course.idx in I.assigned_course_idxs:
            assigned_instructors.append(I)

    if not assigned_instructors:
        raise Exception(
            f"Error! No assigned instructors for course {course} found!")

    return assigned_instructors


def _get_unique_Instr_Timeslot_Room(assigned_instructors: List[Instructor], course: Course, classes: List[Class], state: StateManager):
    """get unique - `instructor, timeslot, room` - for a new `Class` of given Course

    utility function that, if possible - returns a unique set of `instructor, timeslot, room` that does not conflict with any such set of `instructor, timeslot, room` of any `class` in `classes`.
    raises Exception if not possible
    """
    MAX_RAND_R, MAX_RAND_I_T, MAX_RAND_T = 300, 100, 50
    rand_R_counter, rand_I_T_counter = 0, 0

    instructor, timeslot = _get_unique_Instr_Timeslot(
        assigned_instructors, course, classes, state)

    room = random.choice(state.rooms)

    while True:
        if __Room_Timeslot_conflicts(room, timeslot, classes):
            if rand_R_counter < MAX_RAND_R:
                room = random.choice(state.rooms)
                rand_R_counter += 1
                continue
            elif rand_I_T_counter < MAX_RAND_I_T:
                instructor, timeslot = _get_unique_Instr_Timeslot(
                    assigned_instructors, course, classes, state)
                rand_I_T_counter += 1
                continue
            else:
                for instructor in state.instructors:
                    if not __Instr_Timeslot_conflicts(instructor, timeslot, classes):
                        for room in state.rooms:
                            if not __Room_Timeslot_conflicts(room, timeslot, classes):
                                return (instructor, timeslot, room)
                    else:
                        for _ in range(MAX_RAND_T):
                            timeslot = _get_Timeslot_for_Course_Instr(
                                course, instructor, classes, state)
                            if timeslot != None:
                                for room in state.rooms:
                                    if not __Room_Timeslot_conflicts(room, timeslot, classes):
                                        return (instructor, timeslot, room)

                        for timeslot in state.timeslots:
                            if not __Instr_Timeslot_conflicts(instructor, timeslot, classes):
                                for room in state.rooms:
                                    if not __Room_Timeslot_conflicts(room, timeslot, classes):
                                        return (instructor, timeslot, room)

                raise Exception(
                    f"Input Error! No unique (I, T, R) combination possible for course_idx {course.idx}!")
        else:
            return (instructor, timeslot, room)


def _get_unique_Instr_Timeslot(assigned_instructors: List[Instructor], course: Course, classes: List[Class], state: StateManager):
    """function to get unique Instructor and Timeslot for given Course, if it exists.

    NOTE: must satisfy _I_T_conflicts == False
    """

    MAX_RAND_I = 50
    counter = 0
    instructor = random.choice(assigned_instructors)

    timeslot = _get_Timeslot_for_Course_Instr(
        course, instructor, classes, state)

    while timeslot == None:
        instructor = random.choice(assigned_instructors)
        timeslot = _get_Timeslot_for_Course_Instr(
            course, instructor, classes, state)
        if counter > MAX_RAND_I:
            for instructor in state.instructors:
                timeslot = _get_Timeslot_for_Course_Instr(
                    course, instructor, classes, state
                )
                if timeslot != None:
                    break
            raise Exception(
                f"ERROR! No Timeslot found by `_get_unique_Instr_Timeslot` for: {course}")
        counter += 1

    return (instructor, timeslot)


def _get_Timeslot_for_Course_Instr(
    course: Course,
    instructor: Instructor,
    classes: List[Class],
    state: StateManager
) -> Timeslot:
    """
    NOTE: must satisfy (_I_T_conflicts == False)
    """

    if course.lectures_per_week == 2:
        valid_days = ['ST', 'MW']
        valid_slots = state.daily_slots[:-1]
        # excluding last slot i.e. '18:30-21:30'

    elif course.lectures_per_week == 1:
        if course.course_type.lower() == 'lab':
            valid_days = ['S', 'T', 'M', 'W', 'R']
            valid_slots = state.daily_slots[:-1]
        elif course.course_type.lower() == 'theory':
            valid_days = ['S', 'T', 'M', 'W', 'R']
            valid_slots = state.daily_slots[-1]
        else:
            raise Exception(
                f"ERROR! Invalid Course.course_type param for {course}! Valid answers are 'Lab' or 'Theory' for now.")
    else:
        raise Exception(
            f"ERROR! Invalid Course.lectures_per_week param for {course}! Valid answers are '1' or '2' for now.")

    valid_timeslots = (t for t in state.timeslots
                       if t.day_code in valid_days
                       and t.daily_slot in valid_slots)

    for timeslot in valid_timeslots:
        if not __Instr_Timeslot_conflicts(instructor, timeslot, classes):
            return timeslot

    return None


def __Instr_Timeslot_conflicts(given_I: Instructor, given_T: Timeslot, classes: List[Class]):
    """ return True if (given_I, given_T) exists in classes, else False """
    for c in classes:
        if c.instructor.idx == given_I.idx:
            if c.timeslot.idx == given_T.idx \
                    or c.timeslot.idx in given_T.conflicts_with_idxs:
                return True
    return False


def __Room_Timeslot_conflicts(given_R: Room, given_T: Timeslot, classes: List[Class]):
    """ return True if (given_R, given_T) exists in classes, else False """
    for c in classes:
        if c.room.idx == given_R.idx:
            if c.timeslot.idx == given_T.idx \
                    or c.timeslot.idx in given_T.conflicts_with_idxs:
                return True
    return False
