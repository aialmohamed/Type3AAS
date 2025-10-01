// Subscriber Agent ASL file
// Initial beliefs
interested_in("sensor_data").
interested_in("alerts").

// Initial goals
!start_listening.

// Plans
+!start_listening <- 
    .print("Starting to listen for published data...");
    +listening.

+received_message(Topic, Content) <- 
    .print("Received message from topic ", Topic, ": ", Content);
    !process_message(Topic, Content).

+!process_message(Topic, Content) <- 
    .print("Processing message from ", Topic, ": ", Content).