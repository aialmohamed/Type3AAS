// This is the goal that the FSM's NegotiationState triggers.
// Its only job is to call our custom action.
+negotiate(yes) <-
    .print("BDI engine is handling the !negotiate goal.");
    .check_request. // This calls the .check_request action defined in Python

// This plan is for debugging. It will trigger when the .check_request action
// finishes and adds the negotiation_result belief.
+negotiation_result(Result) <-
    .print("BDI has set negotiation result to: ", Result);
    -negotiation_result(Result). // Clean up the belief so it doesn't re-trigger

// --- The following plans are excellent for debugging ---
// They will print out any new beliefs that the agent acquires.

+current_state(State) <-
  .print("BDI Belief Updated: Current State is : ",State).

+supported_skills(Skills) <-
  .print("BDI Belief Updated: Machine Skills are :",Skills).

+skills_constraints(Constraint) <-
  .print("BDI Belief Updated: Constraints are :",Constraint).

+free_time_slots(FTM) <-
  .print("BDI Belief Updated: Free slots are :", FTM).