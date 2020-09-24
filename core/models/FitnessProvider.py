
from abc import ABC, abstractmethod
from core.models.ConstraintManager import ConstraintManager

class FitnessProvider(ABC):
    def __init__(self, constraint_manager: ConstraintManager):
        self.constraint_manager = constraint_manager

    @abstractmethod
    def fitness(self, schedule, **kwargs) -> float:
        raise NotImplementedError
