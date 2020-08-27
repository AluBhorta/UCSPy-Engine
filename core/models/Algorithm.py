from abc import ABC, abstractmethod

from core.models import StateManager
from core.logging import UCSPLogger


class Algorithm(ABC):
    def __init__(self, logger: UCSPLogger, state: StateManager, name: str):
        self.logger = logger
        self.state = state
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError("Algorithm.run()")
