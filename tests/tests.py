from statistics import mean
from concurrent import futures


from core.parsers.parse_schedule_params import generate_state_from_csv
from core.generators.generate_random_schedule import generate_random_schedule as grs
from core.fitness import default as fitness
from core.models import StateManager


def fitness_job(state: StateManager):
    sch = generate_random_schedule(state)
    return fitness(sch)


def test_process_pool(job, *args, n=100):
    with futures.ProcessPoolExecutor() as e:
        fs = [e.submit(job, *args) for _ in range(n)]

        res = []

        for f in futures.as_completed(fs):
            r = f.result()
            print(r)
            res.append(r)

        print(f"mean: {mean(res)}")
