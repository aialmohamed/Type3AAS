job(sleep).

!init.

+!init <-
  .print("Receiver starting ....");
  .print("Ready to receive jobs...").

+start_work <-
  .print("Receiver: Got work command!");
  -+job(do);
  !doing_somthing.

+!doing_somthing : job(do) <-
  .print("You are wasting time man ! ");
  .wait(1000);
  .print("Receiver is done ! ");
  -+job(sleep).