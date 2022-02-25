
from ..models import Schedule, Class, Section, ScheduleParam


class ScheduleOperator:
    def __init__(self, schedule_param: ScheduleParam):
        self.schedule_param = schedule_param

    def deflatten(self, flat_sch) -> Schedule:
        """ <ndarray(c*5,)> -> Sch """
        return flat_sch.reshape(len(self.schedule_param.sections), 5)

    def numrepr_to_sch(self, numrepr) -> Schedule:
        """ <ndarray(n,5)> -> <Sch> """
        return Schedule(
            classes=[(
                Class(
                    Section(self.schedule_param.get_course(i[0]), i[1]),
                    self.schedule_param.get_instructor(i[2]),
                    self.schedule_param.get_room(i[3]),
                    self.schedule_param.get_timeslot(i[4])
                )
            ) for i in numrepr]
        )

    def flat_to_sch(self, flat_schedule, **kwargs) -> Schedule:
        numrepr = self.deflatten(flat_schedule)
        schedule = self.numrepr_to_sch(numrepr)
        return schedule
