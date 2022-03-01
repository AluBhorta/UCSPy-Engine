# Design

This section describes how UCSPy-Engine formulates and encodes UCSP into a set of models that can be understood by a computer. This allows us to generate, store, or manipulate schedules, as well as to measure and analyze their performance.

## Architecture

The following diagram demonstrates the components of UCSPy-Engine from a high-level, functional perspective:

![](../data/img/UCSP_flowchart.PNG)

The target is to find an optimal Schedule that satisfies our constraints best. But, to get a Schedule as output, we need to provide the necessary input.

## The Inputs

To define a UCSP, we need 2 main inputs:

- the `schedule_param`: which are the required data needed to form a schedule
- and `constraints`: which are what we want to satisfy

### Schedule Params

A `schedule_param` consists of lists of `Courses`, `Instructors`, `Timeslots`, `Rooms`, `CourseGroups`.

#### Course

Represents a particular course (of a subject) in a university e.g. CSE101 is a course.

A course consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `num_of_sections`: number of sections of that course to be offered.
- `lectures_per_week`: how many lectures are offered in a week for this course. A `lecture` represents a physical event in the real world.
- `course_type`: "Lab" or "Theory" (more types could be used).
- `sections`: Reference to the collection of all the Sections.
- `credits`: The credits rewarded for taking this particular course. Currently, the credits are being deduced by the `course_type` attribute, but it could be provided as an input.

#### Section

Sections are used to fulfill the total number of sections to be offered, for a particular course.

A Section consists of:

- `course`: A reference to the course.
- `sec_number`: The section number.

#### Room

A room is a location where a particular section of a course is held (e.g. CSELAB1, GPL, 5012, etc.)

A Room consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `seat_capacity`: the number of students that a room can accommodate.
- `allowed_course_idxs`: a collection of course indices that are allowed in this room.

#### Timeslot

A particular period/interval of time in a week. (e.g. Sun & Tue 08:00-09:30).

A Timeslot consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `day_code`: the code to identify the weekday(s) e.g. "S" for Sunday or "ST" for Sunday+Tuesday.
- `daily_slot`: the daily time slot e.g "08:00-09:30" or "09:40-11:10"
- `conflicts_with_idxs`: the indices of the timeslots which this timeslot conflicts with e.g. "ST,08:00-09:30" conflicts with "S,08:00-09:30" as both are on Sunday on the same slot.

#### Instructor

The teacher/professor/faculty for teaching courses.

An Instructor consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `assigned_course_idxs`: the collection of courses that this Instructor can take or is assigned.
- `preferred_timeslot_idxs`: indices of the timeslots they prefer (used for a soft constraint).
- `min_credit_req`: the minimum credits that should be taken by a particular instructor (used for a soft constraint).

#### CourseGroup

Represents a group of courses.

A CourseGroup consists of:

- `idx`: unique index.
- `desc`: detail description. Can contain meta-information.
- `course_idxs`: a collection of Course indices.
- `preferred_timeslot_idxs`: a collection of Timeslot indices, which are preferred for the courses (used for a soft constraint).

### Constraints

Now let's look at the constraints.

There are 2 types: Hard and Soft. The Hard Constraints must be satisfied to consider a Schedule even viable. The Soft Constraints, when violated, add penalties to the fitness of the Schedule.

The following are the current constraints that UCSPy-Engine holds, which are mostly deduced from our university, IUB.

#### Hard Constraints

1. No two classes can take place in the same room at the same Timeslot.
2. No Instructor can take more than one class at a given Timeslot.

#### Soft Constraints

1. Instructors should only take certain courses they are are assigned to.

2. A particular Room should only allow Classes of certain Courses.

3. CourseGroups have Timeslot preferences.

4. Instructors have Timeslot preferences.

5. If a Course has 2 Lectures Per Week, it should take place in a composite Timeslot i.e. with a Day code of "ST" or "MW".

6. The Lab Section of a Course (if any) should be placed in a Timeslot that is before or after the corresponding Theory Section.

7. Instructors have minimum credit load requirements.

8. The Theory Section and the corresponding Lab Section of a Course (if any) should be taken by the same Instructor.

NOTE:

- institutions can and should adjust the penalties to their needs.
- a Lab course should be directly after its corresponding Theory course in the `courses.csv` schedule_param
- read [this](./modify_constraints.md) to learn more about how to modify/add constraints.

## The Output

#### Class

A Class is the base unit of a schedule that defines a particular event, in space and time.

A Class consists of:

- `section`: The Section (of a Course).
- `instructor`: The Instructor.
- `room`: The Room.
- `timeslots`: The Timeslots. Note the 's' - some courses can have classes that exceed several consecutive periods.

### Schedule

A Schedule represents a solution of the UCSP inputs provided, which consists of:

- `classes`: the collection of all classes. note that the total number of classes is equal to the total number of sections, as they have a 1 to 1 mapping.
- `course_groups`: the CourseGroups. This property was optional but turned out useful for our fitness calculation of individual schedules.

## Fitness Calculation

The fitness of a schedule determines how desirable it is, and how much a Schedule violates the constraints determines its fitness.

The section below describes how the fitness of a Schedule `s` is calculated using the (3) currently available fitness functions:

### TanH

![](../data/img/Tanh.png)

Where a schedule of `1.0` fitness is infeasible, while a fitness of `0.0` is a perfect solution.

### Default

![](../data/img/Default.png)

Where a schedule of `0.0` fitness is infeasible, while a fitness of `1.0` is a perfect solution.

### Default Exponential

![](../data/img/DefaultExpo.png)

Where a schedule of `0.0` fitness is infeasible, while a fitness of `1.0` is a perfect solution.

---

## Extensibility (Advanced)

The system is designed to be flexible, so that it may be customized (with a bit of effort) according to the needs of the institution.

- to add new algorithms - extend the `Algorithm` abstract class
- to add new fitness functions - extend the `FitnessProvider` abstract class
- to modify/add new constraints - read [this](./modify_constraints.md)

You may also decide to change the `DefaultScheduleGenerator` or update the shape of the `ScheduleParam` to suit your needs, but that will require changes to other components of the system as well.

Feel free to open a PR or an Issue if you need help.
