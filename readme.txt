Sign Server

This file contains the server side application for a simulated bus destination sign. This "sign" will display whatever
text string is passed over port 5000 using authorization key b'1234'. The following options are currently available at
initialization:

    1 = default sign (7x128) no scroll
    2 = default sign (7x128) scroll

The scrolling will occur if the desired message is longer than the sign width. Additionally the software reads in the
output letter configuration data from letters.txt at initialization.


Sign Client

This software simulates the client side of a message request to the simulated bus destination sign. At initialization the
client can be configured to send a one time test message, or to run the simulated bus program based on the data input which
gives the bus position every second (locations.csv) and the location data for the stops (stops.json). During transit, the
destination ticker will display the route name as well as the time alternating at 1 second interval. When a destination
is reached, the sign will show "Next Stop:" followed by the destination information for 5 seconds.
