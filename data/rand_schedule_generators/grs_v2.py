from data.models import StateManager, Schedule, Class, Section, Course, Instructor, Timeslot, Room
from typing import List
import numpy as np
import random


def generate_random_schedule_v2(state: StateManager) -> Schedule:
    '''Random schedule generator V2
    '''
    classes = []

    for C in state.courses:
        assigned_instructors = _get_assigned_instructors_for(C, state)

        for sec_i in range(C.num_of_sections):
            instructor, timeslots, room = _get_unique_I_Ts_R(
                assigned_instructors, C, classes, state)

            section = Section(C, sec_i+1)
            classes.append(Class(timeslots, room, section, instructor))

    return Schedule(classes)


def _get_assigned_instructors_for(course: Course, state: StateManager):
    INSTRUCTORS = state.instructors
    course_idx = course.idx

    assigned_instructors = []
    for I in INSTRUCTORS:
        if course_idx in I.assigned_course_idxs:
            assigned_instructors.append(I)

    if not assigned_instructors:
        raise Exception(
            "Error! No assigned instructors for course_idx %s found!" % course_idx)

    return assigned_instructors


def _get_unique_I_Ts_R(assigned_instructors: List[Instructor], course: Course, classes: List[Class], state: StateManager):
    """get unique - `instructor, timeslots, room` - for a new `Class` of given Course

    utility function that, if possible - returns a unique set of `instructor, timeslots, room` that does not conflict with any such set of `instructor, timeslots, room` of any `class` in `classes`.
    if not possible - it raises Exception
    """
    MAX_RAND_R, MAX_RAND_I_Ts, MAX_RAND_Ts = 30, 10, 10
    rand_R_counter, rand_I_T_counter = 0, 0

    instructor, timeslots = _get_unique_I_Ts(
        assigned_instructors, course, classes)

    room = random.choice(state.rooms)

    while True:
        if _R_Ts_conflicts(room, timeslots, classes):
            if rand_R_counter < MAX_RAND_R:
                room = random.choice(state.rooms)
                rand_R_counter += 1
                continue
            elif rand_I_T_counter < MAX_RAND_I_Ts:
                instructor, timeslots = _get_unique_I_Ts(
                    assigned_instructors, course, classes)
                rand_I_T_counter += 1
                continue
            else:
                for instructor in assigned_instructors:
                    if not _I_Ts_conflicts(instructor, timeslots, classes):
                        for room in state.rooms:
                            if not _R_Ts_conflicts(room, timeslots, classes):
                                return (instructor, timeslots, room)
                    else:
                        for _ in range(MAX_RAND_Ts):
                            timeslots = _get_timeslots_for_C_I(
                                course, instructor, classes, state)
                            if not _I_Ts_conflicts(instructor, timeslots, classes):
                                for room in state.rooms:
                                    if not _R_Ts_conflicts(room, timeslots, classes):
                                        return (instructor, timeslots, room)

                raise Exception(
                    f"Input Error! No unique (I, Ts, R) combination possible for course_idx {course.idx}!")
        else:
            return (instructor, timeslots, room)


def _get_unique_I_Ts(assigned_instructors: List[Instructor], course: Course, classes: List[Class], state: StateManager):
    """function to get unique Instructor and Timeslots for given Course, if it exists.

    must make sure that I and Ts don't conflict
    """
    MAX_RAND_Ts, MAX_RAND_I = 10, 30
    rand_I_counter = 0

    instructor = random.choice(assigned_instructors)
    timeslots = _get_timeslots_for_C_I(course, instructor, classes, state)
    # TODO: 
    # 1. instead of checking `_I_Ts_conflicts` in this func, do it in `_get_timeslots_for_C_I`
    # 2. backpropagate upwards as required

    while True:
        if _I_Ts_conflicts(instructor, timeslots, classes):
            if rand_I_counter < MAX_RAND_I:
                instructor = random.choice(assigned_instructors)
                rand_I_counter += 1
                continue
            else:
                for instructor in assigned_instructors:
                    if not _I_Ts_conflicts(instructor, timeslots, classes):
                        return (instructor, timeslots)
                    else:
                        for _ in range(MAX_RAND_Ts):
                            timeslots = _get_timeslots_for_C_I(
                                course, instructor, classes, state)
                            if not _I_Ts_conflicts(instructor, timeslots, classes):
                                return (instructor, timeslots)

                raise Exception(
                    f"Input Error! No unique (I, Ts) combination possible for course_idx {course.idx}!")
        else:
            return (instructor, timeslots)


def _get_timeslots_for_C_I(course: Course, instructor: Instructor, classes: List[Class], state: StateManager) -> List[Timeslot]:
    def _get_start_t_idx(weedkay): return (state.num_of_daily_slots * weedkay)
    def _get_end_t_idx(weedkay): return (
        state.num_of_daily_slots * (weedkay + 1)) - 1

    num_of_weekdays = len(state.timeslots) // state.num_of_daily_slots

    timeslot_idxs = []

    for cls_i in range(course.classes_per_week):
        for weekday in range(num_of_weekdays):
            start_t_idx = _get_start_t_idx(weekday)
            end_t_idx = _get_end_t_idx(weekday)

            consecutive_timeslot_idxs = _get_n_consecutive_timeslot_idxs(
                course.timeslots_per_class, start_t_idx, end_t_idx, classes)
            if consecutive_timeslot_idxs != []:
                timeslot_idxs.extend(consecutive_timeslot_idxs)
                break

    if len(timeslot_idxs) != (course.timeslots_per_class * course.classes_per_week):
        raise Exception(
            f"""Error! Not enough suitable timeslots found for course: {course.desc}.
                timeslot_idxs: {timeslot_idxs}
                len(timeslot_idxs): {len(timeslot_idxs)}
                course.timeslots_per_class: {course.timeslots_per_class}
                course.classes_per_week: {course.classes_per_week}
            """)
        # might need repair mechanism e.g. via shifting single timeslot classes for making room for consecutive classes

    timeslots = [state.get_timeslot(t_idx) for t_idx in timeslot_idxs]
    return timeslots


def _get_n_consecutive_timeslot_idxs(n: int, start_t_idx: int, end_t_idx: int, classes: List[Class]):
    for i in range(start_t_idx, end_t_idx+1):   # TODO
        pass


def _I_Ts_conflicts(I: Instructor, Ts: List[Timeslot], classes: List[Class]):
    # TODO: update to account for timeslot's'
    """ return True if (I, T) exists in S, else false """
    if classes:
        classes = np.array(classes)
        for L in classes[:, (3, 1)]:
            if L[0] == I and L[1] == Ts:
                return True
    return False


def _R_Ts_conflicts(room: Room, timeslots: List[Timeslot], classes: List[Class]):
    # TODO: update to account for timeslot's'
    """ return True if (R, T) already exists in classes, else false """
    if classes:
        classes = np.array(classes)
        for L in classes[:, (0, 1)]:
            if L[0] == room and L[1] == timeslots:
                return True
    return False
