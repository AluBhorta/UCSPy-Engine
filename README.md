# UCSPy-Engine

![](https://travis-ci.com/AluBhorta/UCSPy-Engine.svg?branch=master) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/AluBhorta/UCSPy-Engine/blob/master/LICENSE)

An extensible framework for solving UCSP.

## What Is UCSP?

Every semester a university has to deal with the time consuming and error-prone task of scheduling courses.

The task of assigning every Section of a Course - a Classroom for a given Instructor and Timeslots is a difficult challenge on its own. The difficulty is greatly heightened with the addition of constraints like preferred rooms for a course, or preferred timeslots for an instructor, etc. The list of these (soft) constraints can be enormous for a university, making the task much more difficult.

> The task or problem of scheduling courses of a university is known as the _University Course Scheduling Problem_ or _UCSP_.

UCSP is, in fact, an NP-Complete optimization problem, meaning that figuring out the best possible schedule that satisfies all the constraints is practically impossible most of the time. That is because of the sheer number of possibilities in which a Schedule can be formed increases exponentially with the addition of a new parameter: a new room, or course, etc.

For this reason, standard searching algorithms are incapable of finding a sufficiently good solution. This is a headache for universities and educational institutions.

Fortunately, we are blessed to be living in an age with metaheuristics and other smart searching algorithms. Some examples of smart algorithms include - Genetic Algorithm, Particle Swarm Optimization, Simulated Annealing, Artificial Bee Colony Algorithm, and many others.

### What Is The Point Of UCSPy-Engine?

> The goal of UCSPy-Engine is, to democratize access to smart and easy scheduling solutions & to facilitate innovation towards finding new and improved algorithms.

It does that by doing the heavy lifting of formulating, encoding, and generating the problem into a neat application.

UCSPy-Engine should (in theory) allow any university or educational institution to plug in the parameters and constraints of their semester, and solve their scheduling problem (as long as their schedule parameters are encoded in the form accepted by the engine).

It also allows any smart individuals (like you) who like solving challenging problems - to plug in their own algorithms and achieve better or faster solutions than the algorithms currently available. This gives innovators the platform and possibility to publish their own solutions, at the same time contributing to a worthwhile and interesting problem.

---

### How It Works?

This section describes how UCSPy-Engine formulates and encodes UCSP into a set of models that can be understood by a computer. This allows us to generate, store, or manipulate schedules, as well as to measure and analyze their performance.

Our target is to find an optimal Schedule that satisfies our constraints best. But, in order to get a Schedule as output, we need to provide the necessary input.

![](data/img/UCSP_flowchart.PNG)

### The Inputs

<!-- TODO: revise to check if all models are upto date -->

To define a UCSP, we need 2 main inputs:

- the `schedule params`: which are the required data needed to form a schedule
- and `constraints`: which are what we want to satisfy

The following represents a class diagram of the inputs- Course, Instructor, Room, Timeslot and CourseGroup:
![](data/img/UCSPinput.PNG)

#### Schedule Params

The `schedule params` consists of: `Courses`, `Instructors`, `Timeslots` and `Rooms`. We have one more component called `CourseGroups`, which is specific to the needs of our university i.e. IUB (and maybe to other universities as well).

A breakdown of the information/data held in each component of `schedule params` should be sufficient for working with the engine.

##### Course

Represents a particular course (of a subject) in a university e.g. CSE101 is a course.

A course consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `num_of_sections`: number of sections of that course to be offered.
- `lectures_per_week`: how many lectures are offered in a week. A `lecture` represents a physical event in the real world.
- `course_type`: Lab or Theory (more types can be used).
- `sections`: Reference to the collection of all the Sections.
- `credits`: The credits rewarded for taking this particular course. Currently the credits are being deduced by the `course_type` attribute, but it can be assigned explicitly to individual courses.

##### Section

Sections are used to fulfill the total number of sections to be offered, for a particular course.

A Section consists of:

- `course`: A reference to the course.
- `sec_number`: The section number.

##### Room

Room is a location where a particular section of a course is held (e.g. CSELAB1, GPL, 5012, etc.)

A Room consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `seat_capacity`: you already understand what it is.
- `allowed_course_idxs`: a collection of course indices that are allowed in this room.

##### Timeslot

A particular period/interval of time in a week.

A Timeslot consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `weekday`: The day of the week (Sun-Sat).
- `daily_slot`: A workday is usually divided up into periods or slots e.g. '08:00-09:30' or 'period 1' etc. If there are 7 periods for example, then daily_slot takes a value from 0 to 6.

##### Instructor

The teacher/professor/faculty that takes a particular class.

An Instructor consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `assigned_course_idxs`: the collection of courses that they are assigned.
- `preferred_timeslot_idxs`: timeslots they prefer.
- `min_credit_req`: the minimum credits that should be taken by a particular instructor.

##### CourseGroup

A group of courses, to no ones surprise.

A CourseGroup consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `course_idxs`: a collection of Course indices.
- `preferred_timeslot_idxs`: a collection of Timeslot indices, which are preferred for the courses.

##### Class

A Class is the base unit of a schedule that defines a particular event, in space and time i.e. in room and timeslot(s).

![](data/img/UCSPclass.PNG)

A Class consists of:

- `section`: The Section (of a Course).
- `instructor`: The Instructor.
- `room`: The Room.
- `timeslots`: The Timeslots. Note the 's' - some courses can have classes that exceed several consecutive periods.

NOTE:

- the properties of a `schedule params` component can be modified to suit the needs of a particular university.

#### Constraints

Now let's look at the constraints.

There are 2 types: Hard and Soft. The Hard Constraints must be satisfied to consider a Schedule even viable. The Soft Constraints, when violated, add penalties to the fitness of the Schedule.

The following are the current constraints that UCSPy-Engine holds, which are mostly deduced from our university, IUB.

##### Hard Constraints

1. No two classes can take place in the same room at the same Timeslot.
2. No Instructor can take more than one class at a given Timeslot.

##### Soft Constraints

1. Instructors should only take certain courses they are are assigned to.

2. A particular Room should only allow Classes of certain Courses.

3. CourseGroups have Timeslot preferences.

4. Instructors have Timeslot preferences.

5. If a Course has 2 Lectures Per Week, it should take place in a composite Timeslot i.e. with Day code of "ST" or "MW".

6. The Lab Section of a Course (if any) should be placed in a Timeslot that is before or after the corresponding Theory Section.

8. The Theory Section and the corresponding Lab Section of a Course (if any) should be taken by the same Instructor.

7. Instructors have minimum credit load requirements.

8. The Theory Section and the corresponding Lab Section of a Course (if any) should be taken by the same Instructor.

NOTE:

- institutions can and should adjust the penalties to their needs.
- the Lab course should be directly after its corresponding Theory course in the `courses.csv` schedule_param

### The Output

#### Schedule

A Schedule represents a solution of the UCSP inputs provided, which consists of:

- `classes`: the collection of all classes. You might realize that the total number of classes is equal to the total number of sections, as they have a 1 to 1 mapping.
- `course_groups`: the CourseGroups. This property was optional but turned out useful for our fitness calculation of individual schedules.

### Fitness Calculation

The fitness of a schedule determines how desirable it is, and how much a Schedule violates the constraints determines its fitness.

<!-- The fitness of Schedule `s` is calculated as follows: -->

There are 3 different fitness functions currently available:

- TanH 

![](data/img/Tanh.png)

Where a schedule of `1.0` fitnes is infeasible, while a fitness of `0.0` is a perfect solution.

- Default 

![](data/img/Default.png)

Where a schedule of `0.0` fitness in infeasible, while a fitness of `1.0` is a perfect solution.

- Default Exponential 

![](data/img/DefaultExpo.png)

Where a schedule of `0.0` fitness in infeasible, while a fitness of `1.0` is a perfect solution. 

---

## How To Use UCSPy-Engine?

Alright! Enough theory. It's time to see how it works!

### Dependencies

- python 3.6 (or above)
- pip

Check whether you have the correct version of python installed with:

```bash
python --version
```

### Installation

Install virtualenv:

```bash
pip install virtualenv
```

Initialize and activate a new python environment with virtualenv:

```bash
# For Linux/Unix
virtualenv .venv
source .venv/bin/activate
```

```powershell
# For Windows
python -m virtualenv .venv
.venv\Scripts\activate
```

Install requirements using pip

```bash
pip install -r requirements.txt
```

### Usage

There are 3 main services offered by UCSPy-Engine:

- `solve` - used to solve a course scheduling problem.
- `plot` - used to plot the performance of the solver.
- `inspect` - use to inspect the quality of the solution provided, by showing detail constraint violations.

#### `solve`

The main use case for UCSPy-Engine is to solve a course scheduling problem.

**Configuration**

The parameters required for solving UCSP are provided through a JSON configuration file named `ucsp.config.json` at the root of the project. The following are the main options:

- flags

  - `save_logs`: will save the logs if set to `true`.
  - `save_schedule`: will save the final schedule if set to `true`.
  - `inspect_final_schedule`: will inspect the final schedule if set to `true`.

- `fitness`

  - `min_acceptable_fitness`: the minimum acceptable fitness required to terminate if maximum iterations is not yet completed. Range is from 1-0, 1 being worst solution and 0 being perfect solution.
  - `functions`: (read only) list of available fitness functions names.
  - `use`: the name of the fitness function to use.

- `algorithm`

  - `algorithms`: (read only) list of available algorithm names.
  - `use`: the name of the algorithm to use.

- `constraints`

  - `soft_constraints`

    - `constraints`
      - `id`: (read only) The ID of the soft constraint.
      - `desc`: (read only) the description of the soft constraint.
      - `unit_penalty`: Unit penalty value for the soft constraint. Adjust this to set the priority of the constraints. Range is 0.0-1.0, 0.0 being no penalty and 1.0 being max penalty.
    - `use_ids`: list of the soft constraint IDs to use.

  - `hard_constraints`
    - `constraints`
      - `id`: (read only) The ID of the hard constraint.
      - `desc`: (read only) the description of the hard constraint.
    - `use_ids`: list of the hard constraint IDs to use.

- `schedule_param`
  There are two strategies for providing the schedule_param, `discrete_files` & `folder`.

  `discrete_files` requires the path to each schedule_param file, namely: `rooms_file, timeslots_file, courses_file, instructors_file, coursegroups_file.`

  `folder` accepts the path to a folder that contains the required schedule_param files names as `'rooms.csv', 'timeslots.csv', 'courses.csv', 'instructors.csv', 'course_groups.csv'`.

  - `strategies`: list of length 2 containing the strategies.
    - `name`: (read only) The name of the strategy.
    - `path`: (for folder strategy) path to the folder that contains the required schedule_param files as mentioned above
    - `*_file`: (for discrete_files strategy) path to each schedule_param file as mentioned above.
  - `use_strategy`: name of the strategy to use.

**Running the solver through the cli**

To solve UCSP, use the `solve` command along with the sub-command for the algo, like so:

```sh
python cli.py solve <algo>
```

The available algorithms as of now are:

| solver sub-command | algorithm         |
| ------------------ | ----------------- |
| ga                 | Genetic Algorithm |
| meme               | Memetic Algorithm |

To use Genetic Algorithm, for example, run:

```sh
python cli.py solve ga
```

This will run the Genetic Algorithm using the default parameters, and print out the final schedule.

**Customizing parameters of the algorithm**

Each algorithm has a set of unique parameters that can provided as command line arguments.

For Genetic Algorithm:

| algo parameter  | description                                                                |
| --------------- | -------------------------------------------------------------------------- |
| epochs          | the maximum number of iterations before termination. (default: 100)        |
| population_size | The size of the population in a generation. (default: 100)                 |
| elite_pct       | The % of elites in the population. (default: 10)                           |
| mateable_pct    | The % of population that have a chance to perform crossover. (default: 50) |
| mutable_pct     | The % of population that could be mutated. (default: 20)                   |

For Memetic Algorithm:

| algo parameter   | description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| epochs           | the maximum number of iterations before termination. (default: 100)                  |
| population_size  | The size of the population in a generation. (default: 100)                           |
| elite_pct        | The % of elites in the population. (default: 10)                                     |
| mateable_pct     | The % of population that have a chance to perform crossover. (default: 50)           |
| lcl_search_pct   | The % of population that performs local search. (default: 10)                        |
| lcl_search_iters | The number of iterations of local search for each selected individual. (default: 30) |

For example, the number of iteration could easily be changed to 500 like so:

```sh
python cli.py solve --save-sch=True <algo>
```

The other parameter can be updated as well like so:

```sh
python cli.py solve --save_logs=True <algo>
```

#### `plot`

When solver is run with the `save_logs` flag set to true, it'll save the logs generated in a file under the folder `data/logs/` with the datetime as the log's name `<datetime>.log`.

These generated logs can be used to automatically generate performance plots like this:

![sample-log-plot](data/img/sample-log-plot.png)

And it is done by using the `plot` command, which takes the path of the log file like so:

```sh
python cli.py plot <filpath>
```

To plot from the sample log file, for example, run:

```sh
python cli.py plot data/logs/sample.log
```

Neat right?

#### `inspect`

When solver is run with the `save_schedule` flag set to true, it'll save the final schedule in two forms as csv - one in numerical form (e.g. `sch-num-<datetime>.csv`), and the other in a human readable string form (e.g. `sch-str-<datetime>.csv`).

For example, to inspect the fitness of a schedule named `sch-num-2020-09-03T10-41-37.csv`, run:

```bash
python cli.py inspect data/schedules/sch-num-2020-09-03T10-41-37.csv
```

This will show the constraint violations and the final fitness.

NOTE:

- Make sure you select the correct schedule_param that was used to generate the schedule in the first place.

#### Advanced

UCSPy-Engine is very flexible, and allows you to customize it according to your needs.

<!-- TODO: (describe in detail) -->

- adding new algorithms: extend `Algorithm` abstract class
- adding new fitness function: extend `FitnessProvider` abstract class
- adding new constraints
- adding new Sch Generator
- updating schedule param

For help or synopsis:

```bash
python cli.py -
python cli.py --help

python cli.py - <command>
python cli.py - <command> --help

python cli.py - <command> <subcommand> --help
```

**NB:**

- it is very important that your schedule_params follow the standard order and notation as shown in the default params.
- all `.csv` files are ignored by git as mentioned in the `.gitignore` patterns, except for the default schedule_params. You may update your `.gitignore` to track yours.

---

## Contributing To UCSPy-Engine

Contributions to UCSPy-Engine are welcome! You can make pull requests to the `master` branch.

## License

MIT.
