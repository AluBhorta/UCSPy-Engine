
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

<!-- TODO: (fix tone - 'you') -->

---

<!-- TODO: possibly link or include the thesis paper -->
