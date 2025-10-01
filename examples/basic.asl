// Basic ASL file for BDI agent
// Initial goal
!start.

// Plan to handle the start goal
+!start : true
    <- .print("BDI Agent started with ASL reasoning");
       +car(red);
       .print("The car is ", car(X));
       +truck(blue);
       .print("Added truck belief").

+car(Color)
 <- .print("The car is ",Color).