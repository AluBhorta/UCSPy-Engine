"""
1. Some courses should be taught in particular rooms -> Course.$prefered_rooms.  | Penalty: e.g. 9
    - N.B: some courses might have 0 preffered_rooms, in that case, allow any room

2. All Lectures of a course should be in the same room if they are being offered more than once a week.  | Penalty: e.g. 5

3. (optional) Minimize consecutive lectures i.e. spread out lectures over available Timeslots.   | Penalty: 3
Q. HOW does one measure spread? Standard Dev / Interquartile range?

4. (optional) instructors prefer certain rooms I.preffered_rooms

"""


SOFT_CONSTRAINTS = []
