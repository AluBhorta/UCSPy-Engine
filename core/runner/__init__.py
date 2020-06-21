
from core.parsers.parse_csv import generate_state_from_csv
from algorithms.genetic.ga import genetic_algorithm
from algorithms.pso.pso import particle_swarm_optimization

ALGO_MAPPINGS = {
    "genetic": genetic_algorithm,
    "pso": particle_swarm_optimization,
    # "firefly": "",
    # "memetic": "",
}


def run_ucsp(
    algo="genetic",
    epochs=50,
    population_size=100,
    *args, **kwargs
):
    state = generate_state_from_csv()
    _algo_func = ALGO_MAPPINGS.get(algo)
    if not _algo_func:
        raise Exception(
            "ERROR! Invalid algo name! Inspect Map of available names from ALGO_MAPPINGS in 'core.runner' module.")

    return _algo_func(
        state=state,
        epochs=epochs,
        population_size=population_size,
        *args, **kwargs
    )
