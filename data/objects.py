from data.data import ROOMS as R, TIMESLOTS as T, COURSES as C, INSTRUCTORS as I

from data.models import Room, Timeslot, Course, Instructor, StateManager

# TODO: generate param objects when parsing csv
Rooms = [Room(r[0], r[1]) for r in R]
Timeslots = [Timeslot(t[0], t[1]) for t in T]
Courses = [Course(c[0], c[1], c[2], c[3], c[4]) for c in C]
Instructors = [Instructor(i[0], i[1], i[2], i[3], i[4], i[5]) for i in I]
Batches = []

state_manager = StateManager(Rooms, Timeslots, Courses, Instructors, Batches)
