from typing import List
from pandas import read_csv
import os

from core.models import Room, Timeslot, Course, Instructor, CourseGroup, ScheduleParam, Section
from core.util import _str_to_array


def parse_schedule_params(schedule_param_config) -> ScheduleParam:

    if schedule_param_config['use_strategy'] == "folder":

        st = next(
            s for s in schedule_param_config['strategies'] if s['name'] == 'folder')
        _path = st['path']

        r_fname = "rooms.csv"
        t_fname = "timeslots.csv"
        c_fname = "courses.csv"
        i_fname = "instructors.csv"
        cg_fname = "course_groups.csv"
        try:
            R_DF = read_csv(os.path.join(
                os.getcwd(), _path, r_fname))
            T_DF = read_csv(os.path.join(
                os.getcwd(), _path, t_fname))
            C_DF = read_csv(os.path.join(
                os.getcwd(), _path, c_fname))
            I_DF = read_csv(os.path.join(
                os.getcwd(), _path, i_fname))
            CG_DF = read_csv(os.path.join(
                os.getcwd(), _path, cg_fname))
        except:
            raise Exception(
                f"ERROR! Required files not found in {_path}. They should be named as follows: {r_fname, t_fname, c_fname, i_fname, cg_fname}"
            )

    elif schedule_param_config['use_strategy'] == 'discrete_files':
        st = next(
            s for s in schedule_param_config['strategies'] if s['name'] == 'discrete_files')

        try:
            R_DF = read_csv(os.path.join(
                os.getcwd(), st['files']['rooms_file']))
            T_DF = read_csv(os.path.join(
                os.getcwd(), st['files']['timeslots_file']))
            C_DF = read_csv(os.path.join(
                os.getcwd(), st['files']['courses_file']))
            I_DF = read_csv(os.path.join(
                os.getcwd(), st['files']['instructors_file']))
            CG_DF = read_csv(os.path.join(
                os.getcwd(), st['files']['coursegroups_file']))
        except:
            raise Exception(
                f"ERROR! Failed to make schedule_param from discrete_files!"
            )
    else:
        raise Exception(
            f"ERROR! Invalid schedule_param strategy given!"
        )

    ROOMS = R_DF.to_numpy()
    TIMESLOTS = T_DF.to_numpy()
    COURSES = C_DF.to_numpy()
    INSTRUCTORS = I_DF.to_numpy()
    COURSE_GROUPS = CG_DF.to_numpy()

    """ parse collections """

    return _get_parsed_schedule_param(
        (ROOMS, TIMESLOTS, COURSES, INSTRUCTORS, COURSE_GROUPS)
    )


def _get_parsed_schedule_param(param_collection) -> ScheduleParam:
    ROOMS, TIMESLOTS, COURSES, INSTRUCTORS, COURSE_GROUPS = param_collection
    all_theory_courses = list(filter(lambda x: x[4] == "Theory", COURSES))
    all_theory_course_indices = [c[0] for c in all_theory_courses]

    # Rooms - col 3: allowed_courses
    for i in range(len(ROOMS)):
        allowed_course_idxs = ROOMS[i][3]
        if allowed_course_idxs == "ALL_THEORY":
            allowed_course_idxs = all_theory_course_indices
        elif allowed_course_idxs[:4] == "NOT:":
            not_allowed_courses = [int(i)
                                   for i in allowed_course_idxs[4:].split(',')]
            allowed_course_idxs = []
            for c in range(len(COURSES)):
                if c not in not_allowed_courses:
                    allowed_course_idxs.append(c)
        else:
            allowed_course_idxs = [int(i)
                                   for i in allowed_course_idxs.split(',')]
        ROOMS[i][3] = allowed_course_idxs

    # Instructors - col 2, 3
    for i in range(len(INSTRUCTORS)):
        INSTRUCTORS[i][2] = _str_to_array(INSTRUCTORS[i][2])
        INSTRUCTORS[i][3] = _str_to_array(INSTRUCTORS[i][3])

    # CourseGroups - col 2, 3
    for i in range(len(COURSE_GROUPS)):
        COURSE_GROUPS[i][2] = _str_to_array(COURSE_GROUPS[i][2])
        COURSE_GROUPS[i][3] = _str_to_array(COURSE_GROUPS[i][3])

    '''
    NOTE: the following sanity check can be deduced: (if NUM_OF_LECS_BEING_OFFERED > MAX_LECS_THAT_CAN_BE_OFFERED)
    '''

    for i in range(len(TIMESLOTS)):
        if TIMESLOTS[i][3] == '-':
            TIMESLOTS[i][3] = []
        elif len(TIMESLOTS[i][3]) == 1:
            TIMESLOTS[i][3] = [int(TIMESLOTS[i][3])]
        else:
            TIMESLOTS[i][3] = _str_to_array(TIMESLOTS[i][3])

    Rooms = [Room(r[0], r[1], r[2], r[3]) for r in ROOMS]
    Timeslots = [Timeslot(t[0], t[1], t[2], t[3]) for t in TIMESLOTS]
    Courses = [Course(c[0], c[1], c[2], c[3], c[4]) for c in COURSES]
    Instructors = [Instructor(i[0], i[1], i[2], i[3], i[4])
                   for i in INSTRUCTORS]
    CourseGroups = [CourseGroup(cg[0], cg[1], cg[2], cg[3])
                    for cg in COURSE_GROUPS]

    sections = _get_all_sections(Courses)
    daily_slots = _get_all_daily_slots(Timeslots)
    day_codes = _get_all_day_codes(Timeslots)

    return ScheduleParam(Rooms, Timeslots, Courses, Instructors, CourseGroups, sections, daily_slots, day_codes)


def _get_all_sections(courses: List[Course]) -> List[Section]:
    sections = []
    for c in courses:
        sections.extend(c.sections)
    return sections


def _get_all_daily_slots(ts: List[Timeslot]):
    ds = []
    for t in ts:
        if t.daily_slot not in ds:
            ds.append(t.daily_slot)
    return ds


def _get_all_day_codes(ts: List[Timeslot]):
    dc = []
    for t in ts:
        if t.day_code not in dc:
            dc.append(t.day_code)
    return dc
