!start.

+!start <-
    .get_current_state;
    -start;
    +current_state(free);
    !running_job_plan.


+!running_job_plan: current_state(free)  <-
    .print("Detected Free state -> starting job");
    .print("Running job plan triggered");
    .running_job;
    .print("Job done").

+current_state(State) <-
    .print("Current AAS State: ", State).

+drill_result(Result) <-
    .print("Drilling result: ", Result).