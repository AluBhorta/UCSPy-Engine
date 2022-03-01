# What is UCSP?

Every semester a university has to deal with the time consuming and error-prone task of scheduling courses.

> The task of scheduling courses of a university is known as the _University Course Scheduling Problem_ (UCSP).

The challenge of assigning every Section of a Course - a Classroom for a given Instructor and Timeslots is a difficult obstacle on its own. This difficulty is greatly heightened with the addition of constraints like preferred rooms for a course, or preferred timeslots for an instructor, etc. The list of these (soft) constraints can be enormous for a university, making the task much more difficult.

UCSP is, in fact, an NP-Complete optimization problem, meaning that figuring out the best possible schedule that satisfies all the constraints is practically impossible most of the time. That is because the number of possibilities in which a Schedule can be formed increases exponentially with the addition of a new parameter e.g. like a new room, or course, etc.

Yet, many universities still solve this problem manually i.e. by hand. This was indeed the case for our university (IUB).

## What is the goal of UCSPy-Engine?

> The goal of UCSPy-Engine is to provide a simple application to universities for solving their UCSP, and to provide a research platform for facilitating the invention of new and improved optimization algorithms.

It does this by doing the heavy lifting of formulating, encoding, and generating the problem into an extensible application capable of automatically generating solutions i.e. schedules.

UCSPy-Engine should (in theory) allow any university or educational institution to plug in the parameters and constraints of their semester, and solve their scheduling problems. It should also provide a platform for researchers or innovators to work on their own optimization algorithms to achieve better or faster solutions, or to publish their own work.

## Our findings

The application was initially designed for researching about meta-heuristics (like evolutionary algorithms), since standard searching algorithms usually do not suffice for solving such optimization problems.

Using Memetic algortihm for 2000 epochs, we were able to generate a solution to the UCSP of IUB with a **94.75%** contraint satisfaction.

To learn more about our research, [read our undergraduate thesis paper](https://drive.google.com/file/d/1KpuisM6VrlYdBKxrghdEPd3qcqUCOMCz/view?usp=sharing).
