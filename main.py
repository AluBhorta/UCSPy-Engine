from pprint import pprint

from core.runner import run_ucsp


def test():
    pass


if __name__ == "__main__":
    # test()
    sch = run_ucsp(
        # "smart_mut_ga", 
        # "memetic",
        "pso", 
        population_size=100,
    )

    pass
