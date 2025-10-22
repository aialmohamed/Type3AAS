something_todo(no).

!init.

+!init <- 
  .print("starting Simple Agent ...");
  .wait(3000);
  !check_task.

+!check_task : something_todo(no) <-
  .print("Telling the reciver that i am free !");
  .send("simplereciver@localhost", tell, start_work);
  !do_something.

+!do_something <-
  .print("Done .... ").