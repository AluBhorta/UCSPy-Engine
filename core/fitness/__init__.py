from .TanhFitnessProvider import TanhFitnessProvider
from .AckleyFitnessProvider import AckleyFitnessProvider

FITNESS_PROVIDERS = {
    "tanh": TanhFitnessProvider,
    "ackley": AckleyFitnessProvider,
}
