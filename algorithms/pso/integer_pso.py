
# Import standard library
import logging

# Import modules
import numpy as np
import multiprocessing as mp

from pyswarms.backend.operators import compute_pbest, compute_objective_function
from pyswarms.backend.topology import Ring
from pyswarms.backend.handlers import BoundaryHandler, VelocityHandler
from pyswarms.base import DiscreteSwarmOptimizer
from pyswarms.utils.reporter import Reporter


class IntegerPSO(DiscreteSwarmOptimizer):
    def __init__(
        self,
        n_particles,
        dimensions,
        options,
        # bounds=None,
        # bh_strategy="periodic",
        init_pos=None,
        velocity_clamp=None,
        vh_strategy="unmodified",
        # center=1.00,
        ftol=-np.inf,
    ):
        """Initialize the swarm

        Attributes
        ----------
        n_particles : int
            number of particles in the swarm.
        dimensions : int
            number of dimensions in the space.
        options : dict with keys :code:`{'c1', 'c2', 'k', 'p'}`
            a dictionary containing the parameters for the specific
            optimization technique
                * c1 : float
                    cognitive parameter
                * c2 : float
                    social parameter
                * w : float
                    inertia parameter
                * k : int
                    number of neighbors to be considered. Must be a
                    positive integer less than :code:`n_particles`
                * p: int {1,2}
                    the Minkowski p-norm to use. 1 is the
                    sum-of-absolute values (or L1 distance) while 2 is
                    the Euclidean (or L2) distance.
        init_pos : numpy.ndarray, optional
            option to explicitly set the particles' initial positions. Set to
            :code:`None` if you wish to generate the particles randomly.
        velocity_clamp : tuple, optional
            a tuple of size 2 where the first entry is the minimum velocity
            and the second entry is the maximum velocity. It
            sets the limits for velocity clamping.
        vh_strategy : String
            a strategy for the handling of the velocity of out-of-bounds particles.
            Only the "unmodified" and the "adjust" strategies are allowed.
        ftol : float
            relative error in objective_func(best_pos) acceptable for
            convergence
        """
        # Initialize logger
        self.rep = Reporter(logger=logging.getLogger(__name__))
        # Assign k-neighbors and p-value as attributes
        self.k, self.p = options["k"], options["p"]
        # Initialize parent class
        super(IntegerPSO, self).__init__(
            n_particles=n_particles,
            dimensions=dimensions,
            binary=False,
            options=options,
            init_pos=init_pos,
            velocity_clamp=velocity_clamp,
            ftol=ftol,
        )
        # Initialize the resettable attributes
        self.reset()
        # Initialize the topology
        self.top = Ring(static=False)
        self.vh = VelocityHandler(strategy=vh_strategy)
        self.name = __name__

    def optimize(self, objective_func, iters, n_processes=None, **kwargs):
        """Optimize the swarm for a number of iterations

        Performs the optimization to evaluate the objective
        function :code:`f` for a number of iterations :code:`iter.`

        Parameters
        ----------
        objective_func : function
            objective function to be evaluated
        iters : int
            number of iterations
        n_processes : int, optional
            number of processes to use for parallel particle evaluation
            Defaut is None with no parallelization.
        kwargs : dict
            arguments for objective function

        Returns
        -------
        tuple
            the local best cost and the local best position among the
            swarm.
        """
        self.rep.log("Obj. func. args: {}".format(kwargs), lvl=logging.DEBUG)
        self.rep.log(
            "Optimize for {} iters with {}".format(iters, self.options),
            lvl=logging.INFO,
        )
        # Populate memory of the handlers
        self.vh.memory = self.swarm.position

        # Setup Pool of processes for parallel evaluation
        pool = None if n_processes is None else mp.Pool(n_processes)

        self.swarm.pbest_cost = np.full(self.swarm_size[0], np.inf)
        for i in self.rep.pbar(iters, self.name):
            # Compute cost for current position and personal best
            self.swarm.current_cost = compute_objective_function(
                self.swarm, objective_func, pool, **kwargs
            )
            self.swarm.pbest_pos, self.swarm.pbest_cost = compute_pbest(
                self.swarm
            )
            best_cost_yet_found = np.min(self.swarm.best_cost)
            # Update gbest from neighborhood
            self.swarm.best_pos, self.swarm.best_cost = self.top.compute_gbest(
                self.swarm, p=self.p, k=self.k
            )
            # Print to console
            self.rep.hook(best_cost=self.swarm.best_cost)
            # Save to history
            hist = self.ToHistory(
                best_cost=self.swarm.best_cost,
                mean_pbest_cost=np.mean(self.swarm.pbest_cost),
                mean_neighbor_cost=np.mean(self.swarm.best_cost),
                position=self.swarm.position,
                velocity=self.swarm.velocity,
            )
            self._populate_history(hist)
            # Verify stop criteria based on the relative acceptable cost ftol
            relative_measure = self.ftol * (1 + np.abs(best_cost_yet_found))
            if (
                np.abs(self.swarm.best_cost - best_cost_yet_found)
                < relative_measure
            ):
                break
            
            # print(self.swarm.velocity)
            # print(self.swarm.position)
            old_p = self.swarm.position

            # Perform position velocity update
            self.swarm.velocity = self.top.compute_velocity(
                self.swarm, self.velocity_clamp, self.vh
                # ,bounds=None
            )
            self.swarm.position = self._compute_position(self.swarm)
            
            new_p = self.swarm.position
            r = np.array_equal(old_p, new_p)
            print(r)

        # Obtain the final best_cost and the final best_position
        final_best_cost = self.swarm.best_cost.copy()
        final_best_pos = self.swarm.pbest_pos[self.swarm.pbest_cost.argmin()].copy(
        )
        self.rep.log(
            "Optimization finished | best cost: {}, best pos: {}".format(
                final_best_cost, final_best_pos
            ),
            lvl=logging.INFO,
        )
        return (final_best_cost, final_best_pos)

    def _compute_position(self, swarm, bounds=None, bh=BoundaryHandler(strategy="periodic")):
        """Update the position matrix of the swarm

        This computes the next position in a binary swarm. It compares the
        sigmoid output of the velocity-matrix and compares it with a randomly
        generated matrix.

        Parameters
        ----------
        swarm: pyswarms.backend.swarms.Swarm
            a Swarm class
        """

        # TODO: update your position here accordingly
        # X = X + np.floor(V).astype(int)

        try:
            temp_position = swarm.position.copy()

            # temp_position += swarm.velocity
            temp_position += np.floor(swarm.velocity).astype(int)

            if bounds is not None:
                temp_position = bh(temp_position, bounds)

            position = temp_position
        except AttributeError:
            rep.logger.exception(
                "Please pass a Swarm class. You passed {}".format(type(swarm))
            )
            raise
        else:
            return position

    def _sigmoid(self, x):
        """Helper method for the sigmoid function

        Parameters
        ----------
        x : numpy.ndarray
            Input vector for sigmoid computation

        Returns
        -------
        numpy.ndarray
            Output sigmoid computation
        """
        return 1 / (1 + np.exp(-x))
