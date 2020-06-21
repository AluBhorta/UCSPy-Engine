
from core.parsers.parse_csv import generate_state_from_csv
from algorithms.genetic.ga import genetic_algorithm
from algorithms.genetic.smart_mut_ga import smart_mut_genetic_algorithm
from algorithms.pso.pso import particle_swarm_optimization
from algorithms.memetic.memetic import memetic_algorithm

ALGO_MAPPINGS = {
    "ga": genetic_algorithm,    # useless
    "smart_mut_ga": smart_mut_genetic_algorithm,
    "pso": particle_swarm_optimization,
    "memetic": memetic_algorithm,
}


def run_ucsp(
    algo="smart_mut_ga",
    epochs=100,
    population_size=100,
    min_acceptable_fitness=1,
    *args, **kwargs
):
    state = generate_state_from_csv()
    memetic_algorithm.__name__
    _algo_func = ALGO_MAPPINGS.get(algo)
    print(f"Starting UCSP runner using '{_algo_func.__name__}'...\n")
    if not _algo_func:
        raise Exception(
            "ERROR! Invalid algo name! Inspect Map of available names from ALGO_MAPPINGS in 'core.runner' module.")

    return _algo_func(
        state=state,
        epochs=epochs,
        population_size=population_size,
        *args, **kwargs
    )
