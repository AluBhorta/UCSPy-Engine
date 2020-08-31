
from core.models.ScheduleGenerator import ScheduleGenerator
from ..generate_random_schedule import generate_random_schedule
from core.models import ScheduleParam

class DefaultScheduleGenerator(ScheduleGenerator):
    def __init__(self, schedule_param: ScheduleParam):
        super(DefaultScheduleGenerator, self).__init__(schedule_param)

    def generate(self):
        return generate_random_schedule(self.schedule_param)
