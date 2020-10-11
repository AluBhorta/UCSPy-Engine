from .TanhFitnessProvider import TanhFitnessProvider
from .AckleyFitnessProvider import AckleyFitnessProvider
from .DefaultFitnessProvider import DefaultFitnessProvider
from .DefaultExpoFitnessProvider import DefaultExpoFitnessProvider

FITNESS_PROVIDERS = {
    "tanh": TanhFitnessProvider,
    "default": DefaultFitnessProvider,
    "default_expo": DefaultExpoFitnessProvider,
    "ackley": AckleyFitnessProvider,    # experimental
}
