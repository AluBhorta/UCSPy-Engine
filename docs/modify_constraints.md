# Modify Constraints

Hard and Soft constraints can only be included or excluded via the `use_ids` json configuration parameter (`constraints.hard_constraints.use_ids` & `constraints.soft_constraints.use_ids`).

Each Soft constraint additionally require a `unit_penalty` parameter (0.0-1.0). The higher the `unit_penalty`, the more it is given preference relative to other soft contraints.

---

The following sections describe how to add new constraints.

## Add new: hard constraint

- write a hard contraint function (of the following signature), and preferably store it under [this folder](../core/constraints/hard/)

  ```py
  violates_hard_constraint_N: (schedule: Schedule) -> bool
  ```

  - perform desired violation check on Schedule
  - if violates, return True else return False

  NOTE: check out existing hard constraint functions to get a better idea

- add your function to the end of the list [HARD_CONSTRAINT_FUNCS](../core/constraints/__init__.py) with an `id` and `desc` (description)
- add the details your custom hard contraint to [json configuration file](../ucsp.config.json) (`constraints.hard_constraints.constraints`)
- update the `use_ids` list value in the json config to include the `id` your custom hard contraint function (`constraints.hard_constraints.use_ids`)

## Add new: soft constraint

- write a soft contraint function (of the following signature), and preferably store it under [this folder](../core/constraints/soft/)

  ```py
  penalty_of_soft_constraint_N: (
    schedule: Schedule,
    schedule_param: ScheduleParam,
    unit_penalty: float,
    _inspect: bool = False
  ) -> float
  ```

  - perform desired violation check on the Schedule
  - count the number of times the Schedule violates your constraint
  - return the overall penalty from your function `(n * unit_penalty)`

  NOTE: check out existing soft constraint functions to get a better idea

- add your function to the end of the list [SOFT_CONSTRAINT_FUNCS](../core/constraints/__init__.py) with `id`, default `unit_penalty`, and `desc` (description)
- add the details your custom soft contraint to [json configuration file](../ucsp.config.json) (`constraints.soft_constraints.constraints`), including the `unit_penalty`
- update the `use_ids` list value in the json config to include the `id` your custom soft contraint function (`constraints.soft_constraints.use_ids`)
