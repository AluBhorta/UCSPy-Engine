
from data.input_as_csv.parse_csv import generate_state_from_csv

from data.rand_schedule_generators.grs_v2 import generate_random_schedule_v2
from fitness.fitness import fitness

from statistics import mean
from concurrent import futures


state = generate_state_from_csv()


def job(state):
    sch = generate_random_schedule_v2(state)
    return fitness(sch)


def test_process_pool(n=500):
    with futures.ProcessPoolExecutor() as e:
        fs = [e.submit(job, state) for _ in range(n)]

        res = []

        for f in futures.as_completed(fs):
            r = f.result()
            print(r)
            res.append(r)

        print(f"mean: {mean(res)}")
