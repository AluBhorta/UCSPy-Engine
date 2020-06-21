from pprint import pprint
import fire
import os

from core.parsers.parse_csv import generate_state_from_csv
from core.models import Schedule
from algorithms.genetic.smart_mut_ga import smart_mut_genetic_algorithm
from algorithms.memetic.memetic import memetic_algorithm
from algorithms.pso.pso import particle_swarm_optimization
import datetime


class UCSPEngine:
    """
    UCSP Engine

    Solves univesity course scheduling problems using various intelligent algorithms.
    """

    def __init__(
        self,
        params_folder="data/schedule_params/default/",
        out=""
    ):
        self._state = generate_state_from_csv(params_folder)
        self._out = out

    def ga(
        self,
        epochs=100,
        population_size=100,
        min_acceptable_fitness=1,
        elite_pct=10,
        mateable_pct=50,
        mutable_pct=20
    ):
        """ Genetic Algorithm """
        print("Running Genetic Algorithm...\n")
        sch = smart_mut_genetic_algorithm(
            self._state,
            epochs_,
            population_size,
            min_acceptable_fitness,
            elite_pct,
            mateable_pct,
            mutable_pct
        )
        self._write_schedule(sch)

    def memetic(
        self,
        epochs=100,
        min_acceptable_fitness=1,
        population_size=100,
        elite_pct=10,
        mateable_pct=50,
        lcl_search_pct=10,
        lcl_search_iters=30
    ):
        """ Memetic Algorithm """
        print("Running Memetic Algorithm...\n")
        sch = memetic_algorithm(
            self._state,
            epochs=_100,
            min_acceptable_fitness=1,
            population_size=100,
            elite_pct=10,
            mateable_pct=50,
            lcl_search_pct=10,
            lcl_search_iters=30,
        )
        self._write_schedule(sch)

    def pso(
        self,
        epochs=100,
        population_size=20,
        min_acceptable_fitness=1,
        w0=0.8, wf=0.2, c1=1, c2=2, vmax_pct=5
    ):
        """ Particle Swarm Optimization """
        print("Running Particle Swarm Optimization...\n")
        sch = particle_swarm_optimization(
            self._state,
            epochs_,
            population_size,
            min_acceptable_fitness,
            w0, wf, c1, c2, vmax_pct
        )
        self._write_schedule(sch)

    def _write_schedule(self, sch: Schedule):
        if self._out != "":
            t = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

            fname = f"{self._out}schedule-{t}.csv" \
                if self._out[-1] == '/' \
                else f"{self._out}/schedule-{t}.csv"
            fname = os.path.join(os.getcwd(), fname)

            with open(fname, "w") as f:
                f.write(sch.to_csv())

            print(f"Successfully saved schedule to {fname}\n")
        else:
            print("\nFinal Schedule: \n")
            print(sch)


if __name__ == "__main__":
    fire.Fire(UCSPEngine)
    pass
