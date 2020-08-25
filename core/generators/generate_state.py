
import numpy as np
from pandas import read_csv
import os
import json

from core.models import Room, Timeslot, Course, Instructor, CourseGroup, StateManager, ScheduleParam
from core.fitness import FITNESS_FUNCS
from core.generators.generate_constraints import generate_constraints
from core.parsers.parse_schedule_params import parse_schedule_params
from core.generators.generate_random_schedule import generate_random_schedule


def generate_state_manager(schedule_param_config, constraints_config=None, fit_func_name="default") -> StateManager:

    schedule_param = parse_schedule_params(schedule_param_config)

    HARD_CONSTRAINTS, SOFT_CONSTRAINTS = generate_constraints(
        constraints_config)

    return StateManager(
        schedule_param,
        HARD_CONSTRAINTS,
        SOFT_CONSTRAINTS,
        FITNESS_FUNCS.get(fit_func_name),
        generate_random_schedule
    )

from core.parsers.parse_config import parse_config_file

def generate_state_from_config(config_file="ucsp.config.json"):
    _config = parse_config_file(config_file)

    schedule_param_config = _config['schedule_param']
    fit_func_name = _config['fitness']['use'] or "default"
    constraints_config = _config['constraints']

    return generate_state_manager(
        schedule_param_config,
        constraints_config,
        fit_func_name
    )
