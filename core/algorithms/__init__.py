from .genetic.GeneticAlgorithm import GeneticAlgorithm
from .memetic.MemeticAlgorithm import MemeticAlgorithm

ALL_ALGORITHMS = {
    "ga": GeneticAlgorithm,
    "meme": MemeticAlgorithm,
}
