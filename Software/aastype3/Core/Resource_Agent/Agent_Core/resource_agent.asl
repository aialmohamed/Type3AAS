

//////////////////////// PLANS 

!setup.

// initilze the agent and grabe the needed beliefs
+!setup <-
  .print("Agent started : Drilling Machine 1");
  .initialize_agent;
  .check_request.
  

// Upon reciving CFP from Production agent we gonna process the cfp and update the cfp data 
+is_cfp_received(true) <-
  -is_cfp_received(true);
  .print("EVENT: CFP received , procssing the cfp");
  //.process_cfp.
  .process_time_slots.

// Upon processing the cfp 
+is_cfp_valid(false) <-
  -is_cfp_valid(false);
  .print("Either mismatch skill or constarint violated or state is not idle , informing the PA !");
  .inform_production_agent.


+is_cfp_valid(true) <-
  -is_cfp_valid(true);
  .print("No violation -> processong Timeslots").
  //.process_time_slots.

+snap_back_to_listen(true) <-
  -snap_back_to_listen(true);
  .print("Violation Message sent , snapping back to check request");
  .check_request.





//////////////////////////////////////////////////////////////////////////////////////
// debugging


+is_cfp_received(State) <-
  .print("BDI: is_cfp_received changed to ", State).

+is_cfp_valid(State) <-
  .print("BDI: is_cfp_valid changed to ", State).

+current_state(State) <- 
  .print("BDI Belief Updated: Current state is :",State).

+supported_skills(Skills) <-
  .print("BDI Belief Updated: Machine Skills are :",Skills).

+skills_constraints(Constraint) <-
  .print("BDI Belief Updated: Constraints are :",Constraint).

+skills_constraints_types(Types)  <-
  .print("BDI Belief Updated: Constraints Types are :",Types).

+free_time_slots(FTM) <-
  .print("BDI Belief Updated: Free slots are :", FTM).

+booked_time_slots(BTM) <-
  .print("BDI Belief Updated: Book slots are :", BTM).

+cfp_skill(Skill) <-
  .print("CFP Skills : " , Skill).

+cfp_at_time(At_time) <-
  .print("CFP time slot : " , At_time).

+cfp_input_arguments(Args) <-
  .print("CFP input arguments : " , Args).

