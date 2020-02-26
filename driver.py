
from data.generate_random_schedule import generate_random_schedule, generate_random_schedule_v2 as grs2

from fitness.fitness import fitness

from utility import get_algo


def run_ucsp(epochs=50, population_size=128, algo="ga", **kwargs):

    algo = get_algo("ga")
    schedule = algo(epochs=50, population_size=128, **kwargs)

    print(schedule)  # TODO: Pretty Print the final schedule
    print("\nFinal Fitness %f" % fitness(schedule))


def init():
    # from data.models import Room, Timeslot, Course, Instructor, DAO
    from data.objects import LOCAL_DAO as Dao

    # print(Dao.rooms)
    # print(Dao.timeslots)
    print(repr(Dao.courses[0]))
    # print(repr(Dao.instructors[0]))


if __name__ == "__main__":
    init()
    # run_ucsp(epochs=50, population_size=128, algo="ga")
    pass
