
from . import Schedule, Class, Section, ScheduleParam


class ScheduleOperator:
    def __init__(self, schedule_param: ScheduleParam):
        self.schedule_param = schedule_param

    def deflatten(self, flat_sch) -> Schedule:
        """ ndarray<(c*5,)> -> Sch """
        flat_sch.shape = (len(self.schedule_param.sections), 5)
        return flat_sch

    def numrepr_to_sch(self, numrepr) -> Schedule:
        """ ndarray<(n,5)> -> Sch """
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

    # NOTE: could implement 
    # def flat_fitness(self, flat_schedule, **kwargs) -> float:
    #     raise NotImplementedError
    #  &
    # def numrepr_fitness(self, numrepr_schedule, **kwargs) -> float:
    #     raise NotImplementedError
