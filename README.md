# UCSPy-Engine

An extensible framework for solving UCSP, by Farhim Ferdous & Jbeans.

## What Is UCSP?

Every semester a university has to deal with the time consuming and error prone task of scheduling courses. The task of assigning every Section of a Course - a Classroom for a given Instructor and Timeslots is a difficult challenge on its own. And the difficulty is greatly heightened with the addition of constraints like: preferred rooms for a course, or preferred timeslots for an instructor etc. The list of these (soft) constraints can be enormous for a university, making the task much more difficult.

> This task or problem is known as the _University Course Scheduling Problem_, or _UCSP_.

UCSP is in fact, an NP-Complete optimization problem, meaning that figuring out the best possible schedule that satisfies all the constraints is practically impossible most of the time. That is because the sheer number of possibilities in which a Schedule can be formed, increases exponentially with the addition of a new room, or course for example.

For this reason, standard searching algorithms are incapable of finding a suffciently good solution. This is a headache for a universities and educational institutions.

### What Is The Point Of UCSPy-Engine?

Fortnately, we are blessed to be living in an age with metaheuristics and other smart searching algorithms. Some examples of smart algorithms include - Genetic Algorithm, Particle Swarm Optimization, Simulated Annealing, Artificial Bee Colony Algorithm, and many others.

The goal of UCSPy-Engine is, to democratize access of smart and easy scheduling solutions & to facilitate innovation towards finding new and improved algorithms. It does that by doing the heavy lifting of formulating, encoding and generating the problem into a neat application.

UCSPy-Engine should (in theory) allow any university or educational-institution to plug in the parameters and constraints of their semester, and solve their scheduling problem (as long as their schedule_parameters are encoded properly by the engine).

It also allows any smart individuals (like you) who like solving challenging problems, to plug in their own algorithm and achieve better or faster solutions. This gives innovators the platform and possibility to publish their own solutions, at the same time contributing to a worthwhile and interesting problem.

### How It Works?

### Models

...

### Fitness

...

#### Constraints

##### Hard Constraints

1. No two classes can take place in the same room at the same Timeslot (R, T)
1. No instructor can take more than one class at a given Timeslot (I, T)

To add a new hard constraint

- write a func that takes a Schedule as param
- perform desired violation check on Schedule
- if violates, return True else return False
- add your func to the list HARD_CONSTRAINTS at the end

##### Soft Constraints

1. [0.9] Instructors should only take certain courses they are are assigned to
   (I.assigned_course_idxs)

1. [0.85] A particular Room should only allow Classes of certain Courses
   (R.allowed_course_idxs)

1. [0.8] CourseGroups have Timeslot preferences.
   (CG.preferred_timeslot_idxs)

1. [0.6] Instructors have Timeslot preferences.
   (I.preferred_timeslot_idxs)

To add a new soft constraint

- write a func that takes param: (Schedule S, float unit_penalty)
- perform desired violation check on Schedule
- count the number of times S violates your constraint
- return (n \* unit_penalty) from your func
- add your func to the list SOFT_CONSTRAINTS at the en

inputs to ucsp-engine: i.e. schedule params -> the classes/models
output: Classes form -> Schedule
constraints allow calculation of -> fitness
the algorithms

## How To Use UCSPy-Engine?

### Dependencies

- python 3.6 (or above)
- pip
- virtualenv

### Installation

initialize and activate new python environment with virtualenv

```bash
# For Linux/Unix
virtualenv -p `which python3.6` .venv
source .venv/bin/activate
```

```powershell
# For Windows
python -m virtualenv .venv
.venv\Scripts\activate
```

install requirements using pip

```bash
pip install -r requirements.txt
```

### Usage

TODO: add doc for
- solver
- plot

Run `main.py` with command and appropriate flags.

```bash
python main.py <command>
```

| command | algorithm                   |
| ------- | --------------------------- |
| ga      | Genetic Algorithm           |
| memetic | Memetic Algorithm           |
| pso     | Particle Swarm Optimization |

To run Genetic Algorithm for example, run:

```bash
python main.py ga
```

The default schedule_params are in `data/schedule_params/default/`. To specify your own schedule params, use:

```bash
python main.py --params_folder=path/to/your/schedule/params ga
```

For help or synopsis:

```bash
python main.py --help
# Or
python main.py <command> --help
```

**NB:**

- all `.csv` files are ignored by .gitignore, except for the default schedule_params.
- whe running in
  when recording results

---

## How To Contribute To UCSPy-Engine?

UCSPy-Engine Open sourced under the MIT license.

Contributions to UCSPy-Engine are welcome. So feel free to hack, modify or encode your own way or add new algorithms. Make pull requests to the `master` branch.

## License

MIT.
