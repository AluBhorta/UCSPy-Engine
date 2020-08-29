
from abc import ABC, abstractmethod


class FitnessProvider(ABC):
    @abstractmethod
    def fitness(self, schedule, **kwargs) -> float:
        raise NotImplementedError

    @abstractmethod
    def flat_fitness(self, flat_schedule, **kwargs) -> float:
        raise NotImplementedError

    @abstractmethod
    def numrepr_fitness(self, numrepr_schedule, **kwargs) -> float:
        raise NotImplementedError
