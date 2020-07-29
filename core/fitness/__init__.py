from core.fitness.default import fitness as default


FITNESS_FUNCS = {
    "default": default
}

# fitness = FITNESS_FUNCS.get(func_name, "default")
fitness = default
