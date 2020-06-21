# UCSP Engine

UCSP Engine by AluBhorta & Jbeans.

## Usage

### Dependencies

- python 3
- pip
- virtualenv

### Installation

initialize and activate new `python 3` environment with virtualenv (for gnu/linux systems)

```bash
# for Linux/Unix
virtualenv -p `which python3` .venv
source .venv/bin/activate
```

install requirements using pip

```bash
pip install -r requirements.txt
```

### Running

Run `main.py` with command and appropriate flags.

```bash
python main.py <command>
```

| command | algorithm                   |
| ------- | --------------------------- |
| ga      | Genetic Algorithm           |
| memetic | Memetic Algorithm           |
| pso     | Particle Swarm Optimization |

For example:

```bash
python main.py ga
```

For help or synopsis:

```bash
python main.py --help
# OR
python main.py <command> --help
```

**NB:**

- all `.csv` files are ignored by git, except for default schedule_params in `data/schedule_params/default/`.

---

## UCSP Encoding Details

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

---

## License

MIT.
