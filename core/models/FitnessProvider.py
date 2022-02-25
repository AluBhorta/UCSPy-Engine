
from abc import ABC, abstractmethod
from core.services.ConstraintManager import ConstraintManager


class FitnessProvider(ABC):
    def __init__(self, constraint_manager: ConstraintManager):
        self.constraint_manager = constraint_manager

    @abstractmethod
    def fitness(self, schedule, **kwargs) -> float:
        """ 
        return the fitness value of the schedule passed as an arg
        """
        raise NotImplementedError

    @abstractmethod
    def compare(self, fitness1, fitness2) -> bool:
        """ 
        return True if fitness1 is better than fitness2, else False
        """
        raise NotImplementedError

    def is_reverse(self) -> bool:
        """ 
        return True if smaller fitness values are better than larger ones, else False
        """
        return self.compare(0, 1)
