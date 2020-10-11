from .TanhFitnessProvider import TanhFitnessProvider
from .AckleyFitnessProvider import AckleyFitnessProvider
from .DefaultFitnessProvider import DefaultFitnessProvider

FITNESS_PROVIDERS = {
    "tanh": TanhFitnessProvider,
    "ackley": AckleyFitnessProvider,
    "default": DefaultFitnessProvider,
}
