from time import perf_counter
from numpy import array


def bench_time(func, l):
    print(func, l)

    def inner(*args, **kwargs):
        t1 = perf_counter()
        r = func(*args, **kwargs)
        t2 = perf_counter()
        print(f"Time taken for '{func.__name__}': {round(t2-t1, 4)} s")
        return r
    return inner


def _str_to_array(str_values):
    values = []
    for i in str_values.split(","):
        if i != '':
            values.append(int(i))
    return array(values)


def _get_theory_lab_course_idx_paris(courses):
    """ NOTE: for this to work, the Lab course should should be directly after its corresponding Theory course  in the `courses.csv` schedule_param
    TODO: replace the indexing strategy with a dedicated parameter in Course instance (e.g. C.lab_of_course_idx)
    """
    pairs = []
    for crs in courses:
        if crs.course_type.lower() == "lab":
            pairs.append((crs.idx-1, crs.idx))
    return pairs


def _get_classes_of_course_idx(c_idx, schedule):
    return [c for c in schedule.classes
            if c.section.course.idx == c_idx]
