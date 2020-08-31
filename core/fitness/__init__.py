from core.fitness.default import default_fitness
from core.fitness.def_expo import default_expo_fitness
from .tanh_fitness import tanh_fitness
from .TanhFitnessProvider import TanhFitnessProvider

FITNESS_FUNCS = {
    "tanh_fitness": tanh_fitness,
}

FITNESS_PROVIDERS = {
    "tanh_fitness": TanhFitnessProvider,
}
