# Modify Constraints

<!-- TODO -->

you can: add, update or delete constaints. although we recommend you to not delete, instead to not include it on the ucsp config file.

## To add a new hard constraint

- write a new violates func that takes a Schedule as param
- perform desired violation check on Schedule
- if violates, return True else return False
- add your func to the list HARD_CONSTRAINTS at the end


## To add a new soft constraint

- write a func that takes param: (Schedule S, float unit_penalty)
- perform desired violation check on Schedule
- count the number of times S violates your constraint
- return (n \* unit_penalty) from your func
- add your func to the list SOFT_CONSTRAINTS at the en
