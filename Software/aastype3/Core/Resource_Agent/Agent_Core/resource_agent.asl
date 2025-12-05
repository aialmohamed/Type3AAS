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
  .print("EVENT: CFP received , procssing Time slots");
  .process_time_slots;
  .process_cfp.

// Upon processing the cfp 

+is_negotiation_message_ready(true) <-
  -is_negotiation_message_ready(true);
  .print("Informing the PA with the Negotation Resoponse");
  .inform_production_agent;
  .handle_negotiation_response.


+is_negotiation_response_positive(true) <-
  -is_negotiation_response_positive(true);
  .print("The negotation was positive -> preparing for excution");
  .prepare_excution.

+is_negotiation_response_positive(false) <-
  -is_negotiation_response_positive(false);
  .print("The negotation was negative -> going back to check_request ");
  .check_request.

+is_ready_for_execution(true)<-
  -is_ready_for_execution(true);
  .print("The Resource is set for excution ! ");
  .excute_task.

+is_ready_for_execution(false)<-
  -is_ready_for_execution(false);
  .print("The Resource is NOT set for excution ! ").

// ============== EXECUTION PLANS (event-driven) ==============

// Start drill operation - first move, then drill
+excute_skills(drill_capability) <-
  -excute_skills(drill_capability);
  +current_operation(drill);
  .print("Drilling - starting move_xy");
  .move_xy.

// Start movexy-only operation
+excute_skills(movexy_capability) <-
  -excute_skills(movexy_capability);
  +current_operation(movexy);
  .print("Moving");
  .move_xy.

// When move completes during drill operation, start drilling
+move_xy_completed(true) : current_operation(drill) <-
  -move_xy_completed(true);
  .print("Move completed, now drilling");
  .drill.

// When move completes during movexy-only operation, we're done
+move_xy_completed(true) : current_operation(movexy) <-
  -move_xy_completed(true);
  -current_operation(movexy);
  .print("Move completed, operation done");
  .operation_done.

// When drill completes, we're done
+drill_completed(true) <-
  -drill_completed(true);
  -current_operation(drill);
  .print("Drill completed, operation done");
  .operation_done.

// ============== END EXECUTION PLANS ==============

+execution_finished(true)<-
  -execution_finished(true);
  .print("Excution is Done , Cleaning .... ");
  .on_done.

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

+new_cfp_proposal(Data) <-
  .print("New CFP proposal: " , Data).

+is_time_slot_booked(State)<-
  .print("Time Slot booked ? " , State).

+is_ready_for_execution(State)<-
  .print("Is resource ready for excution? " , State).

+excute_skills(skills)<-
  .print("Executing ....  ",skills).

+drill_operation_result(DrillResult)<-
  .print("Drilling Result : ",DrillResult).

+move_xy_operation_result(MoveResult)<-
  .print("Movement Result : ",MoveResult).

+execution_finished(State)<-
  .print("Excution Is done , cleaning Up!").

+current_operation(Op) <-
  .print("Current operation set to: ", Op).

+drill_completed(State) <-
  .print("Drill completed event: ", State).

+move_xy_completed(State) <-
  .print("Move XY completed event: ", State).