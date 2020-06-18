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
        assigned_instructors, course, classes, state)

    room = random.choice(state.rooms)

    while True:
        if _R_Ts_conflicts(room, timeslots, classes):
            if rand_R_counter < MAX_RAND_R:
                room = random.choice(state.rooms)
                rand_R_counter += 1
                continue
            elif rand_I_T_counter < MAX_RAND_I_Ts:
                instructor, timeslots = _get_unique_I_Ts(
                    assigned_instructors, course, classes, state)
                rand_I_T_counter += 1
                continue
            else:  # brute force
                for instructor in assigned_instructors:
                    if not _I_Ts_conflicts(instructor, timeslots, classes):
                        for room in state.rooms:
                            if not _R_Ts_conflicts(room, timeslots, classes):
                                return (instructor, timeslots, room)
                    else:
                        for _ in range(MAX_RAND_Ts):
                            timeslots = _get_timeslots_for_C_I(
                                course, instructor, classes, state)
                            for room in state.rooms:
                                if not _R_Ts_conflicts(room, timeslots, classes):
                                    return (instructor, timeslots, room)

                raise Exception(
                    f"Input Error! No unique (I, Ts, R) combination possible for course_idx {course.idx}!")
        else:
            return (instructor, timeslots, room)


def _get_unique_I_Ts(assigned_instructors: List[Instructor], course: Course, classes: List[Class], state: StateManager):
    """function to get unique Instructor and Timeslots for given Course, if it exists.

    NOTE: must satisfy _I_Ts_conflicts
    """
    MAX_RAND_Ts, MAX_RAND_I = 10, 30
    rand_I_counter = 0

    instructor = random.choice(assigned_instructors)
    timeslots = _get_timeslots_for_C_I(course, instructor, classes, state)

    return (instructor, timeslots)

    # while True:
    #     if _I_Ts_conflicts(instructor, timeslots, classes):
    #         if rand_I_counter < MAX_RAND_I:
    #             instructor = random.choice(assigned_instructors)
    #             rand_I_counter += 1
    #             continue
    #         else:
    #             for instructor in assigned_instructors:
    #                 if not _I_Ts_conflicts(instructor, timeslots, classes):
    #                     return (instructor, timeslots)
    #                 else:
    #                     for _ in range(MAX_RAND_Ts):
    #                         timeslots = _get_timeslots_for_C_I(
    #                             course, instructor, classes, state)
    #                         if not _I_Ts_conflicts(instructor, timeslots, classes):
    #                             return (instructor, timeslots)

    #             raise Exception(
    #                 f"Input Error! No unique (I, Ts) combination possible for course_idx {course.idx}!")
    #     else:
    #         return (instructor, timeslots)


def _get_timeslots_for_C_I(
    course: Course,
    instructor: Instructor,
    classes: List[Class],
    state: StateManager
) -> List[Timeslot]:
    """
        NOTE: must satisfy (_I_Ts_conflicts == False)
    """

    def _get_ts_for_a_class_on(weekday, _tpc, t_idxs):
        tmp_idxs = []

        for ds in range(state.num_of_daily_slots):
            ts = (weekday * state.num_of_daily_slots) + ds
            if ts in t_idxs or _I_Ts_conflicts(instructor, [state.get_timeslot(ts)], classes):
                tmp_idxs = []
            else:
                tmp_idxs.append(ts)

            if len(tmp_idxs) == _tpc:
                return tmp_idxs

        return tmp_idxs if len(tmp_idxs) == _tpc else []

    cpw = course.classes_per_week
    tpc = course.timeslots_per_class
    total_weekdays = len(state.timeslots) // state.num_of_daily_slots

    t_idxs = []

    for _ in range(cpw):
        weekday = 0
        while weekday < total_weekdays:
            _ts = _get_ts_for_a_class_on(weekday, tpc, t_idxs)
            if len(_ts) == tpc:
                t_idxs.extend(_ts)
                break
            else:
                weekday += 1

    if len(t_idxs) == cpw * tpc:
        return [state.get_timeslot(ti) for ti in t_idxs]

    else:
        raise Exception(
            f"ERROR! Not enough timeslots found by `_get_timeslots_for_C_I` for course: {course}.")

    # num_of_weekdays = len(state.timeslots) // state.num_of_daily_slots

    # timeslot_idxs = []

    # # for each class (per week), get `course.timeslots_per_class` number of timeslots
    # for cls_i in range(course.classes_per_week):
    #     for weekday in range(num_of_weekdays):
    #         start_t_idx = _get_start_t_idx(weekday)
    #         end_t_idx = _get_end_t_idx(weekday)

    #         consecutive_timeslot_idxs = _get_n_consecutive_timeslot_idxs(
    #             course.timeslots_per_class,
    #             start_t_idx,
    #             end_t_idx,
    #             classes)
    #         if consecutive_timeslot_idxs != []:
    #             timeslot_idxs.extend(consecutive_timeslot_idxs)
    #             break

    # if len(timeslot_idxs) != (course.timeslots_per_class * course.classes_per_week):
    #     raise Exception(
    #         f"""Error! Not enough suitable timeslots found for course: {course.desc}.
    #             timeslot_idxs: {timeslot_idxs}
    #             len(timeslot_idxs): {len(timeslot_idxs)}
    #             course.timeslots_per_class: {course.timeslots_per_class}
    #             course.classes_per_week: {course.classes_per_week}
    #         """)
    #     # might need repair mechanism e.g. via shifting single timeslot classes for making room for consecutive classes

    # timeslots = [state.get_timeslot(t_idx) for t_idx in timeslot_idxs]
    # return timeslots


# def _get_n_consecutive_timeslot_idxs(n: int, start_t_idx: int, end_t_idx: int, classes: List[Class]):
#     for i in range(start_t_idx, end_t_idx+1):   # TODO
#         pass


def _I_Ts_conflicts(given_I: Instructor, given_Ts: List[Timeslot], classes: List[Class]):
    """ return True if (given_I, given_Ts) exists in classes, else False """
    # if not classes:
    #     raise Exception("ERROR! No Classes provided!")

    for c in classes:
        if c.instructor.idx == given_I.idx:
            for t in c.timeslots:
                given_t_idxs = [i.idx for i in given_Ts]
                if t.idx in given_t_idxs:
                    return True
    return False


def _R_Ts_conflicts(given_R: Room, given_Ts: List[Timeslot], classes: List[Class]):
    """ return True if (given_R, given_Ts) exists in classes, else False """
    # if not classes:
    #     raise Exception("ERROR! No Classes provided!")

    for c in classes:
        if c.room.idx == given_R.idx:
            for t in c.timeslots:
                given_t_idxs = [i.idx for i in given_Ts]
                if t.idx in given_t_idxs:
                    return True
    return False
