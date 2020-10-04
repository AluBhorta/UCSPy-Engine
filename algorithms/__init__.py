from .genetic.GeneticAlgorithm import GeneticAlgorithm
from .memetic.MemeticAlgorithm import MemeticAlgorithm
from .pso.ParticleSwarmOptimization import ParticleSwarmOptimization

ALL_ALGORITHMS = {
    "ga": GeneticAlgorithm,
    "meme": MemeticAlgorithm,
    "pso": ParticleSwarmOptimization,
}
