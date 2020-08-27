from .genetic.smart_mut_ga import GeneticAlgorithm
from .memetic.memetic import MemeticAlgorithm


ALL_ALGORITHMS = {
    "ga": GeneticAlgorithm,
    "meme": MemeticAlgorithm,
}
