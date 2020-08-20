from core.fitness.default import default_fitness
from core.fitness.def_expo import default_expo_fitness
from .tanh_fitness import tanh_fitness

FITNESS_FUNCS = {
    "default": default_fitness,
    "default_expo": default_expo_fitness,
    "tanh_fitness": tanh_fitness,
}

