

def _get_theory_lab_course_idx_paris(courses):
    """ NOTE: for this to work, the Lab course should should be directly after its corresponding Theory course  in the `courses.csv` schedule_param
    alternative way to handle it - replace the indexing strategy with a dedicated parameter in Course instance (e.g. C.lab_of_course_idx)
    """
    pairs = []
    for crs in courses:
        if crs.course_type.lower() == "lab":
            pairs.append((crs.idx-1, crs.idx))
    return pairs


def _get_classes_of_course_idx(c_idx, schedule):
    return [c for c in schedule.classes
            if c.section.course.idx == c_idx]
