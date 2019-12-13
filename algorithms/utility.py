from numpy import concatenate


def flatten(schedule):
    '''flattens a schedule into a 1d array
    the flattening is done across the rows, meaning first all the rooms, then all timeslots, all courses & finally all instructors to be appended to the 1d array
    '''
    return concatenate((schedule[:, 0], schedule[:, 1], schedule[:, 2], schedule[:, 3]), axis=0)
