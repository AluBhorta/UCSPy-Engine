
from core.runner import run_ucsp
from core.parsers.parse_csv import generate_state_from_csv
from core.schedule_generators.grs import generate_random_schedule as grs
from core.fitness.fitness import fitness
from algorithms.genetic.ga import genetic_algorithm


def test():
    state = generate_state_from_csv()
    sch = grs(state)
    sch = genetic_algorithm(state, epochs=100)
    f = fitness(sch)
    print(f"Final fitness: {f}")


if __name__ == "__main__":
    sch = run_ucsp(algo="genetic")
    print(sch)

    # test()
    pass
