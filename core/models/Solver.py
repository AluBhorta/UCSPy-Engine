import os
import datetime

from core.parsers.parse_csv import generate_state_from_csv
from core.models import Schedule
from algorithms.genetic.smart_mut_ga import smart_mut_genetic_algorithm
from algorithms.memetic.memetic import memetic_algorithm
from algorithms.pso.pso import particle_swarm_optimization
from core.logging import UCSPLogger


class UCSPSolver:
    """ 
    UCSP Solver

    used to solve UCSP using preferred algorithms.
    """

    def __init__(
        self,
        params_folder="data/schedule_params/default/",
        save_sch=False,
        save_logs=False,
    ):
        self._state = generate_state_from_csv(params_folder)
        self._logger = UCSPLogger(save_logs)
        self._save_sch = save_sch
        if save_logs:
            self._save_sch = True

    def ga(
        self,
        epochs=100,
        population_size=100,
        min_acceptable_fitness=1,
        elite_pct=10,
        mateable_pct=50,
        mutable_pct=25
    ):
        """ Genetic Algorithm """
        self._logger.write("Running Genetic Algorithm...\n")
        sch = smart_mut_genetic_algorithm(
            self._logger,
            self._state,
            epochs,
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
        population_size=50,
        elite_pct=10,
        mateable_pct=50,
        lcl_search_pct=10,
        lcl_search_iters=30
    ):
        """ Memetic Algorithm """
        self._logger.write("Running Memetic Algorithm...\n")
        sch = memetic_algorithm(
            self._logger,
            self._state,
            epochs,
            min_acceptable_fitness,
            population_size,
            elite_pct,
            mateable_pct,
            lcl_search_pct,
            lcl_search_iters,
        )
        self._write_schedule(sch)

    def pso(
        self,
        epochs=100,
        population_size=100,
        min_acceptable_fitness=1,
        w0=0.8, wf=0.2, c1=1, c2=2, vmax_pct=5
    ):
        """ Particle Swarm Optimization """
        self._logger.write("Running Particle Swarm Optimization...\n")
        sch = particle_swarm_optimization(
            self._logger,
            self._state,
            epochs,
            population_size,
            min_acceptable_fitness,
            w0, wf, c1, c2, vmax_pct
        )
        self._write_schedule(sch)

    def _write_schedule(self, sch: Schedule):
        if self._save_sch:
            t = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
            fname = os.path.join(
                os.getcwd(), "data/schedules", f"schedule-{t}.csv")

            with open(fname, "w") as f:
                f.write(sch.to_csv())

            self._logger.write(
                f"\nEncoded schedule successfully saved to {fname}")
        else:
            self._logger.write("\nFinal Schedule: \n")
            self._logger.write(sch)

    pass
