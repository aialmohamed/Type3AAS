!init.


+!init <- 
  .print("Hello from Drilling Machine 1").

+current_state(State) <-
  .print("Current State is : ",State).

+supported_skills(Skills) <-
  .print("Machine Skills are :",Skills).

+skills_constraints(Constraint) <-
  .print("Constartins are :",Constraint).

+free_time_slots(FTM) <-
  .print("Free slots are :", FTM).

+requested_skills(Skills) <-
  .print("Production Requested Skills are" ,Skills).