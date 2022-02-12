# Configuration

The parameters required for solving UCSP are provided through a JSON configuration file named `ucsp.config.json` at the root of the project. 

The following are the main options:

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
