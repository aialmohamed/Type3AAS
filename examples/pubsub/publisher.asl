// Publisher Agent ASL file
// Initial beliefs
has_data("sensor_data").
publish_interval(5).

// Initial goals
!start_publishing.

// Plans
+!start_publishing <- 
    .print("Starting to publish data...");
    +publishing.

+!publish_data(Topic, Content) <- 
    .print("Publishing to topic ", Topic, ": ", Content);
    +published(Topic, Content).

+published(Topic, Content) <- 
    .print("Successfully published to ", Topic).